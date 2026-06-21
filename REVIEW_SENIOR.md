# Senior Code Review — vaguinhas LinkedIn Bot
**Commits analisados:** HEAD~11..HEAD (últimos 11 commits)  
**Data:** 2026-06-21  
**Revisor:** Claude Sonnet 4.6 (multi-agent, 10 ângulos de análise)

---

## Resumo executivo

O conjunto de commits entregou features reais e úteis (pausa manual, auto-pausa em filtros, detecção de overlay, mapeamentos de CPF/salário/benefícios). A arquitetura geral está correta. Os problemas identificados são de três categorias: **segurança** (CPF em plaintext no source), **confiabilidade** (race condition na pausa, filter_failures incompleto, loop BAT com goto) e **manutenibilidade** (padrão copy-paste de pausa, substring de 2 chars, inconsistência Gemini).

---

## Findings — por severidade

### 🔴 CRÍTICO

#### 1. CPF hardcoded em plaintext no source (2 lugares)
**Arquivo:** `runAiBot.py:780` e `runAiBot.py:1162`  
**Status:** CONFIRMED

```python
elif 'cpf' in label: answer = "***CPF_REMOVIDO***"  # aparece em dois lugares
```

O CPF é um identificador governamental sensível. Está commitado no repositório, aparece em `git diff`, `git log -p`, no console (`questions_list` é printado inteiro), e em qualquer log que capture stdout.

**Correção:** Mover para `config/personals.py` como `cpf = "***CPF_REMOVIDO***"` e referenciar em ambos os lugares.

```python
# config/personals.py
cpf = "***CPF_REMOVIDO***"

# runAiBot.py (nos dois lugares)
elif 'cpf' in label: answer = cpf
```

---

#### 2. `filter_failures` incompleto — maioria dos filtros não conta falhas
**Arquivo:** `runAiBot.py:310-342`  
**Status:** CONFIRMED

`sort_by`, `date_posted` e `easy_apply_only` contam falhas em `filter_failures`. Os demais **não contam**:

- `experience_level`, `job_type`, `on_site`, `location`, `industry`, `job_function`, `job_titles`, `benefits`, `commitments` — via `multi_sel_noWait` que retorna `None`
- `under_10_applicants`, `in_your_network`, `fair_chance_employer` — via `boolean_button_click` sem captura de retorno
- `salary` — `wait_span_click(driver, salary)` retorno descartado (linha 342)

**Cenário de falha:** LinkedIn muda o texto de "Mid-Senior level" para "Sênior" — o filtro falha silenciosamente, `filter_failures = 0`, a pausa nunca ativa, e o bot aplica para vagas sem nenhum dos filtros de experiência configurados.

**Correção:** Ou contar as falhas de `multi_sel_noWait` (precisaria retornar contagem), ou — mais pragmático — verificar após o "Show Results" se os filtros aplicados batem com os configurados.

---

#### 3. `'po' in label` — substring de 2 chars causa falsos positivos
**Arquivo:** `runAiBot.py:752`  
**Status:** CONFIRMED

```python
elif ('po' in label or 'pm' in label) and ('experiência' in label or ...):
    answer = 'Sim'
```

Palavras comuns em português contêm `"po"`: **apo**io, com**po**sto, cam**po** obrigatório, ex**po**rtação, de**po**imento, com**po**nente. Qualquer uma dessas combinada com uma keyword financeira responde `'Sim'` em um campo que pode ser numérico, textual, ou sobre outro assunto.

**Correção:**
```python
# Usar word boundary via regex ou checar token completo
import re
label_tokens = re.split(r'\W+', label)
elif ('po' in label_tokens or 'pm' in label_tokens) and ...:
```

---

### 🟠 ALTO

#### 4. Race condition: `_pause_event.wait()` bloqueia para sempre se stdin fechar após pausa
**Arquivo:** `runAiBot.py:97-113, 297, 352, 373`  
**Status:** PLAUSIBLE (janela de race estreita mas real)

Fluxo do problema:
1. Bot chama `_pause_event.clear()` (filtro falhou)
2. Terminal do usuário é fechado / stdin é redirecionado (`nohup`, pipe)
3. `_pause_listener` recebe `EOFError` e faz `break` — sem chamar `_pause_event.set()`
4. `_pause_event.wait()` na thread principal bloqueia **para sempre**

**Correção:** Adicionar timeout e fallback:
```python
# Em qualquer _pause_event.wait():
if not _pause_event.wait(timeout=3600):  # 1h max
    print("\n[AVISO] Timeout de pausa atingido. Retomando...")
    _pause_event.set()
```

E no listener, ao receber `EOFError`, garantir `set()`:
```python
except EOFError:
    _pause_event.set()  # desbloqueia main thread se estava pausado
    break
```

---

#### 5. BAT: `goto wait_firefox` dentro de bloco `if` aninhado não funciona como esperado
**Arquivo:** `RODAR_BOT.bat:49`  
**Status:** CONFIRMED

```bat
if %errorlevel%==0 (
    echo Fechando Firefox existente...
    ...
    :wait_firefox          <- label DENTRO do bloco
    tasklist ...
    if %errorlevel%==0 (
        timeout /t 2 /nobreak >nul
        goto wait_firefox  <- sai do bloco, re-entra no label
    )
    echo Firefox fechado.
)
```

No CMD, labels são file-scoped, mas o `goto` dentro de um bloco `( )` sai do bloco inteiro e re-entra no label. Na re-entrada, o `if %errorlevel%==0` externo **não é reavaliado** — o código após o label executa diretamente, então `set VAGUINHAS_BROWSER=firefox` roda imediatamente sem checar se Firefox fechou.

**Correção:** Mover o loop para fora do bloco `if`:
```bat
tasklist /FI "IMAGENAME eq firefox.exe" 2>nul | find /I "firefox.exe" >nul
if %errorlevel% neq 0 goto start_ff
echo Fechando Firefox existente...
taskkill /F /IM firefox.exe >nul 2>&1
taskkill /F /IM firefox.exe >nul 2>&1
:wait_firefox
tasklist /FI "IMAGENAME eq firefox.exe" 2>nul | find /I "firefox.exe" >nul
if %errorlevel%==0 ( timeout /t 2 /nobreak >nul & goto wait_firefox )
echo Firefox fechado.
:start_ff
```

---

#### 6. Após pausa por filtros, bot tenta clicar "Mostrar Resultados" que usuário já fechou
**Arquivo:** `runAiBot.py:350-363`  
**Status:** CONFIRMED

Quando `filter_failures > 0`:
1. Bot pausa — usuário aplica filtros manualmente e clica "Mostrar Resultados" (fecha o painel)
2. Usuário digita `p` — bot retoma
3. Bot executa `wait.until(EC.element_to_be_clickable(...show_results_xpath...))` — painel já fechou
4. `TimeoutException` após 3 tentativas → cai no `except Exception` → chama `_pause_event.wait()` **novamente**

**Correção:** Após a pausa por `filter_failures`, pular o "Show Results" click — o usuário já o fez:
```python
if filter_failures > 0:
    _pause_event.clear()
    print(f"\n>>> {filter_failures} FILTRO(S) FALHARAM. Aplique manualmente e clique 'Mostrar resultados'. Depois 'p' + ENTER. <<<\n")
    _pause_event.wait()
    return  # usuário já clicou Show Results, não tentar de novo
```

---

### 🟡 MÉDIO

#### 7. `_pause_thread.start()` no nível do módulo — sem guarda `__main__`
**Arquivo:** `runAiBot.py:112-113`  
**Status:** CONFIRMED

```python
_pause_thread = threading.Thread(target=_pause_listener, daemon=True)
_pause_thread.start()  # executa em qualquer `import runAiBot`
```

Qualquer `import runAiBot` (em teste, REPL, script auxiliar) imediatamente: spawna thread, imprime mensagem na tela, bloqueia stdin.

**Correção:**
```python
if __name__ == "__main__":
    _pause_thread.start()
```
Ou mover o `start()` para dentro da função `main()`.

---

#### 8. Inconsistência: Gemini não recebe carta de apresentação no contexto
**Arquivo:** `runAiBot.py:1243`  
**Status:** CONFIRMED

No mesmo hunk do diff:
```python
user_info_with_letter = get_user_information() + f"\n\nCARTA DE APRESENTAÇÃO...\n{get_cover_letter_text()}"
if ai_provider.lower() == "openai":
    answer = ai_answer_question(..., user_information_all=user_info_with_letter)  # ✅
elif ai_provider.lower() == "deepseek":
    answer = deepseek_answer_question(..., user_information_all=user_info_with_letter)  # ✅
elif ai_provider.lower() == "gemini":
    answer = gemini_answer_question(..., user_information_all=get_user_information())  # ❌ sem carta
```

**Correção:** Substituir `get_user_information()` por `user_info_with_letter` na branch do Gemini.

---

#### 9. `dismiss_confirmation_overlay()` — bare `except: pass` engole crash de sessão
**Arquivo:** `runAiBot.py:1442`  
**Status:** PLAUSIBLE

```python
def dismiss_confirmation_overlay() -> bool:
    try:
        overlay = driver.find_element(...)
        ...
    except: pass  # engole WebDriverException, NoSuchWindowException, etc.
    return False
```

Quando chamada no `finally` (linha 1707) após browser crash, silenciosamente retorna `False`. O `wait_span_click` seguinte lança a exceção real, mas com stack trace que aponta para o `wait_span_click`, não para a causa raiz.

**Correção:**
```python
except NoSuchElementException:
    pass  # overlay não existe — comportamento normal
except Exception as e:
    print_lg(f"[OVERLAY] Erro ao dispensar overlay: {e}")
    return False
```

---

### 🔵 BAIXO / MANUTENÇÃO

#### 10. Padrão `clear/print/wait` copy-pastado 3 vezes
**Arquivo:** `runAiBot.py:297-299, 352-354, 373-375`  
**Status:** CONFIRMED

Mesmo bloco de 3 linhas repetido literalmente. Uma mudança (ex: adicionar timeout, logar para arquivo) precisa ser feita em 3 lugares.

**Correção:**
```python
def _pause_and_wait(message: str) -> None:
    _pause_event.clear()
    print(f"\n>>> {message} <<<\n")
    _pause_event.wait()
```

#### 11. Label de textarea pode capturar texto de tooltip/span decorativo
**Arquivo:** `runAiBot.py:1216`  
**Status:** PLAUSIBLE

O fallback `.//span[@class and not(ancestor::button)]` pega qualquer span com classe que não seja filho de button — inclui tooltips, ícones de ajuda, contadores de caracteres. O primeiro com texto não-vazio "ganha" como label.

**Correção:** Adicionar exclusão de classes conhecidas de UI artefatos:
```python
".//span[not(contains(@class,'artdeco-hoverable')) and not(contains(@class,'visually-hidden')) and @class and not(ancestor::button)]"
```

#### 12. CPF duplicado (já mencionado no finding #1, listado aqui como segundo lugar)
Ver finding #1.

---

## Tabela resumo

| # | Arquivo | Linha | Severidade | Status | Categoria |
|---|---------|-------|------------|--------|-----------|
| 1 | runAiBot.py | 780, 1162 | 🔴 CRÍTICO | CONFIRMED | Segurança |
| 2 | runAiBot.py | 310-342 | 🔴 CRÍTICO | CONFIRMED | Confiabilidade |
| 3 | runAiBot.py | 752 | 🔴 CRÍTICO | CONFIRMED | Correctness |
| 4 | runAiBot.py | 97-113, 297 | 🟠 ALTO | PLAUSIBLE | Confiabilidade |
| 5 | RODAR_BOT.bat | 49 | 🟠 ALTO | CONFIRMED | Correctness |
| 6 | runAiBot.py | 350-363 | 🟠 ALTO | CONFIRMED | Confiabilidade |
| 7 | runAiBot.py | 112-113 | 🟡 MÉDIO | CONFIRMED | Arquitetura |
| 8 | runAiBot.py | 1243 | 🟡 MÉDIO | CONFIRMED | Correctness |
| 9 | runAiBot.py | 1442 | 🟡 MÉDIO | PLAUSIBLE | Confiabilidade |
| 10 | runAiBot.py | 297-375 | 🔵 BAIXO | CONFIRMED | Manutenção |
| 11 | runAiBot.py | 1216 | 🔵 BAIXO | PLAUSIBLE | Correctness |

---

## O que está bem

- Threading com `daemon=True` está correto — thread não impede o processo de fechar
- `_pause_event.wait()` no loop principal é o lugar certo para bloquear (entre jobs, nunca no meio de uma candidatura)
- `dismiss_confirmation_overlay` tenta "voltar" ao formulário antes de usar ESC — comportamento defensivo correto
- `panel_opened` flag detecta falha de abertura de painel antes de tentar clicar filtros
- Label detection para textarea agora usa 4 estratégias em cascata — abordagem correta
- Cover letter incluída no contexto AI para OpenAI e DeepSeek é a solução certa para o problema de "climate change"
