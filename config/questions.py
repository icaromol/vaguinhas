'''
Author:     Sai Vignesh Golla
LinkedIn:   https://www.linkedin.com/in/saivigneshgolla/

Copyright (C) 2024 Sai Vignesh Golla

License:    GNU Affero General Public License
            https://www.gnu.org/licenses/agpl-3.0.en.html
            
GitHub:     https://github.com/GodsScion/Auto_job_applier_linkedIn

Support me: https://github.com/sponsors/GodsScion

version:    26.01.20.5.08
'''


###################################################### APPLICATION INPUTS ######################################################


# >>>>>>>>>>> Easy Apply Questions & Inputs <<<<<<<<<<<

# Give an relative path of your default resume to be uploaded. If file in not found, will continue using your previously uploaded resume in LinkedIn.
default_resume_path = "all resumes/default/resume.pdf"      # (In Development)

# Path to your profile photo (JPG, JPEG, PNG). Leave empty string "" to skip photo upload.
default_photo_path = "all resumes/photo/foto.png"

# Path to your cover letter file (PDF or DOCX). Leave empty string "" to skip cover letter upload.
default_cover_letter_path = "all resumes/cover_letter/cover_letter.pdf"

# What do you want to answer for questions that ask about years of experience you have, this is different from current_experience?
years_of_experience = "5"          # A number in quotes Eg: "0","1","2","3","4", etc.

# Do you need visa sponsorship now or in future?
require_visa = "No"               # "Yes" or "No"

# What is the link to your portfolio website, leave it empty as "", if you want to leave this question unanswered
website = "https://github.com/icaromol"               # "www.example.bio" or "" and so on....

# Please provide the link to your LinkedIn profile.
linkedIn = "https://linkedin.com/in/icaromolinari"              # "https://www.linkedin.com/in/example" or "" and so on...

# What is the status of your citizenship? # If left empty as "", tool will not answer the question. However, note that some companies make it compulsory to be answered
# Valid options are: "U.S. Citizen/Permanent Resident", "Non-citizen allowed to work for any employer", "Non-citizen allowed to work for current employer", "Non-citizen seeking work authorization", "Canadian Citizen/Permanent Resident" or "Other"
us_citizenship = "Other"



## SOME ANNOYING QUESTIONS BY COMPANIES 🫠 ##

# What to enter in your desired salary question (American and European), What is your expected CTC (South Asian and others)?, only enter in numbers as some companies only allow numbers,
desired_salary = 120000           # PJ salary pleno — ~R$10k/mês. Do NOT use quotes
desired_salary_clt = 84000        # CLT salary pleno — ~R$7k/mês (R$6k–R$8k). Do NOT use quotes
'''
Note: If question has the word "lakhs" in it (Example: What is your expected CTC in lakhs), 
then it will add '.' before last 5 digits and answer. Examples: 
* 2400000 will be answered as "24.00"
* 850000 will be answered as "8.50"
And if asked in months, then it will divide by 12 and answer. Examples:
* 2400000 will be answered as "200000"
* 850000 will be answered as "70833"
'''

# What is your current CTC? Some companies make it compulsory to be answered in numbers...
current_ctc = 0                 # 800000, 900000, 1000000 or 1200000 and so on... Do NOT use quotes
'''
Note: If question has the word "lakhs" in it (Example: What is your current CTC in lakhs), 
then it will add '.' before last 5 digits and answer. Examples: 
* 2400000 will be answered as "24.00"
* 850000 will be answered as "8.50"
# And if asked in months, then it will divide by 12 and answer. Examples:
# * 2400000 will be answered as "200000"
# * 850000 will be answered as "70833"
'''

# (In Development) # Currency of salaries you mentioned. Companies that allow string inputs will add this tag to the end of numbers. Eg: 
# currency = "INR"                 # "USD", "INR", "EUR", etc.

# What is your notice period in days?
notice_period = 0                    # Any number >= 0 without quotes. Eg: 0, 7, 15, 30, 45, etc.
'''
Note: If question has 'month' or 'week' in it (Example: What is your notice period in months), 
then it will divide by 30 or 7 and answer respectively. Examples:
* For notice_period = 66:
  - "66" OR "2" if asked in months OR "9" if asked in weeks
* For notice_period = 15:"
  - "15" OR "0" if asked in months OR "2" if asked in weeks
* For notice_period = 0:
  - "0" OR "0" if asked in months OR "0" if asked in weeks
'''

# Your LinkedIn headline in quotes Eg: "Software Engineer @ Google, Masters in Computer Science", "Recent Grad Student @ MIT, Computer Science"
linkedin_headline = "Product Manager | Founder Técnico | SaaS B2B | IA Generativa | Mentor de Produto · Founder Institute" # "Headline" or "" to leave this question unanswered

# Your summary in quotes, use \n to add line breaks if using single quotes "Summary".You can skip \n if using triple quotes """Summary"""
linkedin_summary = """
Product Manager com background técnico completo e mentalidade de founder. Construí a coprodux, um SaaS B2B, do zero — conduzindo discovery, definindo roadmap, liderando um time de 13 pessoas e entregando integrações de IA generativa (OpenAI, Anthropic, Azure AI Foundry) em produção. Cheguei a 25 clientes pagantes e R$60k de aporte. Também sou Mentor de Produto no Founder Institute, maior aceleradora pré-seed do mundo, orientando founders em produto, go-to-market e estratégia técnica.
"""

'''
Note: If left empty as "", the tool will not answer the question. However, note that some companies make it compulsory to be answered. Use \n to add line breaks.
''' 

# Your cover letter in quotes, use \n to add line breaks if using single quotes "Cover Letter".You can skip \n if using triple quotes """Cover Letter""" (This question makes sense though)
cover_letter = """
Olá,

Me candidato a esta vaga com um perfil que une o que poucos candidatos conseguem combinar: visão estratégica de produto, background técnico completo e experiência real de founder.

Nos últimos 2 anos, construí do zero a coprodux, um SaaS B2B de planejamento de comunicação. Atuei simultaneamente como PM e CTO: conduzi discovery com clientes, defini roadmap, priorizei backlog, liderei um time de até 13 pessoas e tomei todas as decisões de arquitetura, stack e infraestrutura. O produto chegou a 25 clientes pagantes, centenas de usuários e recebeu aporte de R$60.000. Também integramos IA generativa (OpenAI, Anthropic e Azure AI Foundry) como funcionalidade entregue em produção.

Paralelamente, atuo há 2 anos como Mentor de Produto no Founder Institute (maior aceleradora pré-seed do mundo), orientando founders em decisões de produto, go-to-market e estratégia técnica.

Meu diferencial não é saber fazer tudo. É saber conectar negócio, tecnologia e usuário sem ruído — e tomar decisões com contexto técnico real, o que elimina o gap entre produto e engenharia no dia a dia.

Ícaro Molinari | icaromolinari@gmail.com | +55 31 98710-2204 | linkedin.com/in/icaromolinari
"""
## >>>>>>>>>>> ENGLISH VERSIONS (used automatically when job description is in English) <<<<<<<<<<<

linkedin_summary_en = """
Product Manager with a full technical background and founder mindset. I built coprodux, a B2B SaaS, from scratch — leading discovery, defining the roadmap, managing a team of 13 people and shipping generative AI integrations (OpenAI, Anthropic, Azure AI Foundry) to production. Reached 25 paying customers and R$60k in funding. I also mentor founders at Founder Institute, the world's largest pre-seed accelerator.
"""

cover_letter_en = """
Hi,

I'm applying for this role with a profile that few candidates can combine: strategic product vision, full technical background, and real founder experience.

Over the last 2 years, I built coprodux from scratch — a B2B SaaS for communication planning — acting simultaneously as PM and CTO. I led customer discovery, defined the roadmap, prioritized the backlog, managed a team of up to 13 people, and made all architecture and infrastructure decisions. The product reached 25 paying customers, hundreds of users, and secured R$60,000 in funding. We also shipped generative AI (OpenAI, Anthropic, Azure AI Foundry) as a production feature.

In parallel, I've been a Product Mentor at Founder Institute (world's largest pre-seed accelerator) for 2 years, guiding founders on product decisions, go-to-market, and technical strategy.

My edge isn't knowing how to do everything. It's connecting business, technology, and users without noise — and making decisions with real technical context, which eliminates the product-engineering gap on a daily basis.

Ícaro Molinari | icaromolinari@gmail.com | +55 31 98710-2204 | linkedin.com/in/icaromolinari
"""

##> ------ Dheeraj Deshwal : dheeraj9811 Email:dheeraj20194@iiitd.ac.in/dheerajdeshwal9811@gmail.com - Feature ------

# Your user_information_all letter in quotes, use \n to add line breaks if using single quotes "user_information_all".You can skip \n if using triple quotes """user_information_all""" (This question makes sense though)
# We use this to pass to AI to generate answer from information , Assuing Information contians eg: resume  all the information like name, experience, skills, Country, any illness etc. 
user_information_all ="""
Nome: Ícaro Molinari
E-mail: icaromolinari@gmail.com
Telefone: +55 31 98710-2204
Localização: Belo Horizonte, MG, Brasil
LinkedIn: https://linkedin.com/in/icaromolinari

RESUMO:
Product Manager com background técnico completo e mentalidade de founder. Construí a coprodux (SaaS B2B) do zero atuando simultaneamente como PM e CTO. 25 clientes pagantes, aporte de R$60k, time de 13 pessoas. Integrei IA generativa (OpenAI, Anthropic, Azure AI Foundry) em produção. Mentor de Produto no Founder Institute há 2 anos.

EXPERIÊNCIA:
- Founder & PM/CTO, coprodux (fev 2024 – mai 2026): SaaS B2B de planejamento de comunicação. Discovery com clientes, roadmap, backlog, arquitetura e liderança de time (13 pessoas). Stack: NestJS, React, Next.js, Tailwind, PostgreSQL, Azure.
- Mentor de Produto, Founder Institute São Paulo (out 2024 – presente): Mentorei 10+ startups em discovery, roadmap, GTM, decisões técnicas e pitch.
- Consultor de Negócios, Grow my Business (ago 2021 – jan 2024): Consultoria estratégica em tech, saúde, varejo e finanças.
- Diretor de Vendas e Marketing, Vida Veda (jun 2023 – fev 2024): +40% de crescimento em receita, +500% em vendas de produto-chave.
- Coordenador de Marketing, V4 Company (set 2022 – jan 2023): Gestão de R$20M/mês em verba. Melhoria de ROI em 85%+ dos clientes.
- Diretor de Marketing, Evolution Marketing (ago 2021 – ago 2022): Dashboard de NPS, pipeline de entrega, portfólio de produtos do zero.

FORMAÇÃO:
- MBA em Liderança Organizacional · Uniamérica (2024)
- FI Core Program · Founder Institute (2024)
- CST em Marketing · Uniamérica (2021–2024)
- Bacharelado em Música · UFMG (2015–2019)

HABILIDADES:
Product Discovery, Estratégia de Roadmap, Priorização de Backlog, OKRs, Scrum, Kanban, Gestão de Stakeholders, Go-to-Market, IA Generativa (LLMs), OpenAI API, Anthropic API, Azure AI Foundry, NestJS, React, Next.js, PostgreSQL, Azure, Decisões orientadas a dados, SaaS B2B

IDIOMAS: Português (nativo), Inglês (profissional completo), Espanhol (profissional completo), Alemão (básico)

PREMIAÇÕES: Inovativa Brasil, Ibmec Hubs
ANOS DE EXPERIÊNCIA: 5
PRETENSÃO SALARIAL: R$84.000/ano CLT | R$120.000/ano PJ
DISPONIBILIDADE: imediata
"""

user_information_all_en = """
Name: Ícaro Molinari
Email: icaromolinari@gmail.com
Phone: +55 31 98710-2204
Location: Belo Horizonte, MG, Brazil
LinkedIn: https://linkedin.com/in/icaromolinari

SUMMARY:
Product Manager with a full technical background and founder mindset. Built coprodux (B2B SaaS) from scratch acting simultaneously as PM and CTO. 25 paying customers, R$60k funding, team of 13 people. Shipped generative AI (OpenAI, Anthropic, Azure AI Foundry) to production. Product Mentor at Founder Institute for 2 years.

EXPERIENCE:
- Founder & PM/CTO, coprodux (Feb 2024 – May 2026): B2B SaaS for communication planning. Customer discovery, roadmap, backlog, architecture and team leadership (13 people). Stack: NestJS, React, Next.js, Tailwind, PostgreSQL, Azure.
- Product Mentor, Founder Institute São Paulo (Oct 2024 – present): Mentored 10+ startups on discovery, roadmap, GTM, technical decisions and pitch.
- Business Consultant, Grow my Business (Aug 2021 – Jan 2024): Strategic consulting in tech, health, retail and finance.
- Sales & Marketing Director, Vida Veda (Jun 2023 – Feb 2024): +40% revenue growth, +500% sales on key product.
- Marketing Coordinator, V4 Company (Sep 2022 – Jan 2023): Managed R$20M/month in ad spend. Improved ROI for 85%+ of clients.
- Marketing Director, Evolution Marketing (Aug 2021 – Aug 2022): NPS dashboard, delivery pipeline, product portfolio from scratch.

EDUCATION:
- MBA in Organizational Leadership · Uniamérica (2024)
- FI Core Program · Founder Institute (2024)
- Tech Degree in Marketing · Uniamérica (2021–2024)
- Bachelor's in Music · UFMG (2015–2019)

SKILLS:
Product Discovery, Roadmap Strategy, Backlog Prioritization, OKRs, Scrum, Kanban, Stakeholder Management, Go-to-Market, Generative AI (LLMs), OpenAI API, Anthropic API, Azure AI Foundry, NestJS, React, Next.js, PostgreSQL, Azure, Data-driven decisions, B2B SaaS

LANGUAGES: Portuguese (native), English (professional), Spanish (professional), German (basic)

AWARDS: Inovativa Brasil, Ibmec Hubs
YEARS OF EXPERIENCE: 5
SALARY EXPECTATION: R$84,000/year CLT | R$120,000/year PJ
AVAILABILITY: immediate
"""
##<
'''
Note: If left empty as "", the tool will not answer the question. However, note that some companies make it compulsory to be answered. Use \n to add line breaks.
''' 

# Name of your most recent employer
recent_employer = "coprodux"       # "", "Lala Company", "Google", "Snowflake", "Databricks"

# Example question: "On a scale of 1-10 how much experience do you have building web or mobile applications? 1 being very little or only in school, 10 being that you have built and launched applications to real users"
confidence_level = "8"             # Any number between "1" to "10" including 1 and 10, put it in quotes ""
##



# >>>>>>>>>>> RELATED SETTINGS <<<<<<<<<<<

## Allow Manual Inputs
# Should the tool pause before every submit application during easy apply to let you check the information?
pause_before_submit = True         # True or False — IMPORTANTE: revise cada candidatura antes de enviar
'''
Note: Will be treated as False if `run_in_background = True`
'''

# Should the tool pause if it needs help in answering questions during easy apply?
# Note: If set as False will answer randomly...
pause_at_failed_question = True    # True or False, Note: True or False are case-sensitive
'''
Note: Will be treated as False if `run_in_background = True`
'''
##

# Do you want to overwrite previous answers?
overwrite_previous_answers = False # True or False, Note: True or False are case-sensitive







############################################################################################################
'''
THANK YOU for using my tool 😊! Wishing you the best in your job hunt 🙌🏻!

Sharing is caring! If you found this tool helpful, please share it with your peers 🥺. Your support keeps this project alive.

Support my work on <PATREON_LINK>. Together, we can help more job seekers.

As an independent developer, I pour my heart and soul into creating tools like this, driven by the genuine desire to make a positive impact.

Your support, whether through donations big or small or simply spreading the word, means the world to me and helps keep this project alive and thriving.

Gratefully yours 🙏🏻,
Sai Vignesh Golla
'''
############################################################################################################