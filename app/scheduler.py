from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import re , resend

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.domain.services.alerts import fetch_active_alerts
from app.domain.services.nearby_station import fetch_nearby_station_weather
from app.integrations.gemini import generate_with_gemini
from app.domain.models import GeminiRequest
from dotenv import load_dotenv


load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")

EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")


scheduler = AsyncIOScheduler()

async def scheduled_weather_report():
    try:
        print("running job: scheduled_weather_report")
        alerts_collector = await fetch_active_alerts()
        nearby_station_report = await fetch_nearby_station_weather()

        scheduled_prompt = f"""
            Você é um assistente meteorológico para a Região Metropolitana do Rio de Janeiro.

            ## Dados disponíveis

            ### Alertas ativos:
            {alerts_collector}

            ### Relatório da estação mais próxima:
            {nearby_station_report}

            ## Sua tarefa

            Com base nos dados acima, responda ao usuário em **português brasileiro** seguindo este formato:

            1. **Saudação** – cumprimente de forma natural e breve
            2. **Situação atual** – resuma as condições do momento : pode incluir informaçoes detalhdas da estação mais próxima, como temperatura, céu e vento etc
            3. **Alertas** – se houver alertas ativos, destaque-os com clareza; se não houver, confirme isso de forma tranquilizadora
            4. **Recomendação** – uma dica prática e objetiva com base nas condições


            ---

        
            """


        response_text = await generate_with_gemini(scheduled_prompt, "gemini-2.5-flash-lite")
        print(alerts_collector)
        print(type(alerts_collector))
        _send_email(response_text)
        print(f"Relatório enviado para {EMAIL_TO}")
    except Exception as e:
        import traceback
        print("Error in scheduled_weather_report:", e) 
        traceback.print_exc()



def _send_email(content: str) -> None:
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
    html = f"<p>{html.replace(chr(10), '<br>')}</p>"

    resend.Emails.send({
        "from": EMAIL_FROM,
        "to": EMAIL_TO,
        "subject": "⛅ Previsão do Tempo – Região Metropolitana do RJ",
        "html": html,
        "text": content
    })

def start_scheduler():
    print("starting scheduler...")
    scheduler.add_job(
        scheduled_weather_report,
        trigger="cron",
        hour=12,
        minute=00,
        id="weather_report"
    )
    scheduler.start()

