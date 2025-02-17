# 2FA Login und Benutzerkonto-Verwaltung - Flask Anwendung
Dieses Projekt kombiniert ein **2FA (Two-Factor Authentication)**-Login-System mit einer übersichtlichen **Benutzerkonto-Verwaltung** und unterstützt die Registrierung sowie das Login basierend auf OTP (One-Time Password) Codes. Es wurde mit dem Flask-Framework entwickelt.
## Wofür ist diese Anwendung? 
Diese Anwendung bietet folgende Hauptfunktionen:
### 1. **2FA Login-System**
- Sichert den Login-Prozess zusätzlich zu Benutzernamen und Passwort durch einen **2FA (TOTP)**-Code.
- Generiert einen QR-Code, den Benutzer mit einer Authenticator-App (z. B. Google Authenticator oder OpenOTP) scannen können, um temporäre Passwörter zu erhalten.

### 2. **Benutzerkonto-Management**
- Nutzer können sich **registrieren**, sich in ihre Konten **einloggen**, ihre 2FA-Einstellungen **ändern** und ihre Konten verwalten.
- Unterstützt die Anzeige und Änderung des **2FA-Status** für mehr Benutzerkontrolle.

## Nutzung der Anwendung 
### 1. Repository klonen 
Klonen Sie das Repository in Ihr Arbeitsverzeichnis:
``` shell
git clone https://github.com/komiklol/2FA_Login-Register
cd 2FA_Login-Register
```
### 2. Umgebung einrichten 
Richten Sie eine virtuelle Umgebung ein, um Abhängigkeiten isoliert zu installieren:
``` shell
# Virtuelle Umgebung erstellen
python -m venv venv

# Aktivieren der virtuellen Umgebung
# Für Windows
venv\Scripts\activate

# Für macOS und Linux
source venv/bin/activate
```
### 3. Abhängigkeiten installieren 
Installieren Sie die erforderlichen Python-Pakete:
``` shell
pip install Flask flask-bcrypt pyotp qrcode[pil]
```
### 4. Anwendung starten
Starten Sie die Flask-Anwendung:
``` shell
flask --app app.py run
```
Die Anwendung ist standardmäßig unter **[http://127.0.0.1:5000](http://127.0.0.1:5000)** erreichbar.
## Routen und Nutzung **(Routes and Usage)**

| **Route**        | **Beschreibung**                                                                       |
|------------------|----------------------------------------------------------------------------------------|
| **`/`**          | Startseite mit Links zur Registrierung oder Login-Seite.                               |
| **`/register`**  | Registrierungsseite: Erlaubt Nutzern, ein Konto zu erstellen und 2FA zu aktivieren.    |
| **`/login`**     | Login-Seite: Prüft Benutzername, Passwort und 2FA-Code und gibt bei Erfolg Zugriff.    |
| **`/account`**   | Benutzerkonto: Zeigt 2FA-Status an und bietet Optionen zur Änderung der Einstellungen. |
| **`/change2fa`** | Seite zur Aktivierung/Deaktivierung von 2FA.                                           |
| **`/logout`**    | Loggt Nutzer aus und beendet die Sitzung.                                              |
## Benutzung des 2FA-Workflows
1. Ein Benutzer kann sich auf der **Registrierungsseite** einen Account erstellen, dabei wird ein QR-Code erstellt.  
2. Der QR-Code kann mit einer Authenticator-App wie [Google Authenticator](https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2) gescannt werden, um Zugriff auf TOTP-Codes zu erhalten.
3. Für das Registrieren wird dieser Code benötigt, der über die Authenticator-App bereitgestellt wird.
4. Wenn im Account die 2FA auf **True** steht, benötigt man seinen Code bei jedem Login. 

## Erforderliche Installation
Für dieses Projekt werden folgende Technologien benötigt:
1. **Python-Bibliotheken**
    - **Flask**: Web Framework zur Entwicklung der Anwendung.
    - **Flask-Bcrypt**: Hashing von Passwörtern zur Sicherung sensibler Daten.
    - **PyOTP**: Implementierung von TOTP, um zeitbasierte 2FA-Codes zu generieren und zu validieren.
    - **qrcode**: Generiert QR-Codes für Benutzer, um ihre Authenticator-App zu synchronisieren.

2. **Zubehör/Tools**
    - **Authenticator-App**: Eine App wie [Google Authenticator](https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2) oder [OpenOTP Token](https://play.google.com/store/apps/details?id=com.rcdevs.auth) wird benötigt, um QR-Codes zu scannen und TOTP-Codes zu generieren.

## Hinweise
- **Sicherheit:** Benutzerinformationen und Passwörter werden sicher mit Bcrypt-Hashing gespeichert.
- **TOTP-Gültigkeit:** Die generierten TOTP-Codes sind standardmäßig für 30 Sekunden gültig.
- **Benutzerfreundlich:** Die Anwendung enthält einfache und intuitive HTML-Formulare für Login, Registrierung und Kontoverwaltung.

## HTML-Vorlagen
Dieses Projekt nutzt benutzerfreundliche und minimalistische **HTML-Vorlagen**:
- **`login.html`:** Seite für den Benutzer-Login.
- **`register.html`:** Seite für die Benutzerregistrierung. Zeigt den QR-Code an.
- **`account.html`:** Seite zur Anzeige des Benutzerkontos und seines aktuellen 2FA-Status.
- **`ErrorPage.html`:** Anzeigen von Fehlermeldungen mit einem Link zur Startseite.

## Viel Spaß! 🚀
