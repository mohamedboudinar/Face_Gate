# FaceGate
FaceGate ist eine Webanwendung, in der fortschrittliche Gesichtserkennungstechnologie die Sicherheit erhöht und das Zeitmanagement am Arbeitsplatz digitalisiert. Unser System ermöglicht es registrierten Nutzern, ihre Identität sicher zu authentifizieren und so nahtlosen und sicheren Zugang zu wichtigen Diensten zu erhalten. Alle Aktivitäten werden sorgfältig über unsere benutzerfreundliche Website verfolgt und verwaltet, was Effizienz und Kontrolle fördert.

## Inhaltsverzeichnis

- [Einführung](#einführung)
- [Funktionen](#funktionen)
- [Technischer Stack](#technischer-stack)
- [Systemanforderungen](#systemanforderungen)
- [Installation](#installation)
- [Ausführen des Projekts](#ausführen-des-projekts)
- [Testkonto](#testkonto)
- [Django-Projekt mit Anaconda](#django-projekt-mit-anaconda)
- [Python-Installation](#python-installation)
- [Installation von Anaconda](#installation-von-anaconda)
- [Verwendung](#verwendung)
- [Lizenz](#lizenz)

## Einführung

Das FaceGate-Projekt ist eine innovative Initiative zur Verbesserung der Sicherheits- und Zugangskontrollsysteme in Unternehmen durch eine webbasierte Plattform, die modernste Gesichtserkennungstechnologie verwendet. Unsere Plattform ermöglicht autorisierten Nutzern einen einfachen und sicheren Zugang zu gesicherten Bereichen und bietet Verwaltungsfunktionen für das Einrichten von Zugangsberechtigungen, die Verwaltung von Nutzerdaten und das Überwachen von Zugangsprotokollen. Sie unterstützt auch die Überprüfung von Arbeitszeiten und die Verwaltung von Urlaubsanträgen. Weiterhin arbeiten wir an einem Prototypen mit integrierten Gesichtserkennungskameras und Türmechanismen, um die Anwendung unserer Technologie zu demonstrieren. Unser Ziel ist es, die Arbeitszeiterfassung und Sicherheitsmaßnahmen zu optimieren und effizienter zu gestalten.

## Funktionen

- Einloggen mit einem bereits existierenden Konto
- Mitarbeiter hinzufügen, löschen und Daten ändern
- Abteilung hinzufügen, löschen und Daten ändern
- Bilder für die Gesichtserkennung in Echtzeit aufnehmen
- Urlaub beantragen
- Krankheitstage beantragen und Bescheinigung hochladen
- Arbeitszeiten einsehen

## Technischer Stack

Geben Sie einen Überblick über die in Ihrem Projekt verwendeten Technologien:

- Frontend: Html,Css,Js,Bootstrap
- Backend: Django, Django Channels
- Datenbank: Sqlite (automatisch von Django generiert )
- Pakete: face-recognition,cmake,materializecssform,dlib

## Systemanforderungen

Betriebssystem:

Windows 10, macOS 10.14 (Mojave) oder höher, Linux (Ubuntu 18.04 oder höher)

Software:

Webbrowser: Google Chrome (Version 90 oder höher), Mozilla Firefox (Version 85 oder höher), Safari (Version 12 oder höher), Microsoft Edge (Version 85 oder höher)
Datenbank: MySQL 5.7 oder höher, PostgreSQL 10 oder höher
Backend: Python 3.7 oder höher, Django 3.2 oder höher, Django Channels 4.1.0 oder höher
Frontend: Node.js 12, 14 oder 16, npm 6 oder höher, React 17 oder höher
Entwicklungsumgebung: Visual Studio Code 1.50 oder höher
Python-Distribution: Anaconda 2020.11 oder höher

Hardwareanforderungen:

Prozessor: 1 GHz oder schneller, 64-Bit-Prozessor (Dual-Core oder besser empfohlen)
Arbeitsspeicher (RAM): Mindestens 2 GB (4 GB oder mehr empfohlen)
Festplattenspeicher: Mindestens 10 GB freier Speicherplatz für die Installation und Betrieb der Anwendung, sowie zusätzlicher Speicherplatz für Backups und zukünftige Updates
Netzwerk: Breitband-Internetverbindung für den Zugriff auf die Webanwendung und die Kommunikation mit der Datenbank

## Installation

1. Öffnen Sie eine Kommandozeile oder ein Terminal und navigieren Sie zu dem Verzeichnis, in dem das Django-Projekt gespeichert ist. Verwenden Sie dazu den Befehl `cd "../07-FaceGate/Software/FaceGate/"`.

2. Erstellen Sie die Umgebung und installieren Sie die notwendigen Komponenten mit dem Befehl: `conda env create -f pythonEnv.yml`

3. Aktivieren Sie die neue Umgebung mit dem Befehl: `conda activate facegate`.

## Ausführen des Projekts

1. Öffnen Sie eine Kommandozeile oder ein Terminal und navigieren Sie zu dem Verzeichnis, in dem das Django-Projekt gespeichert ist. Verwenden Sie dazu den Befehl `cd "../07-FaceGate/Software/FaceGate/"`.

2. Aktivieren Sie die neue Umgebung mit dem Befehl: `conda activate facegate`.

3. Öffnen Sie eine neue Kommandozeile oder ein Terminal und navigieren Sie zu dem Verzeichnis, in dem das Frontend gespeichert ist. Verwenden Sie dazu den Befehl `cd "../07-FaceGate/Software/FaceGate/`.

4. Starten Sie das Backend mit dem Befehl `python manage.py runserver`.


## Testkonto

Hier sind einige Konten, die Sie zum Testen der Anwendung verwenden können:

**Admin-Konto(Superuser):**

- Benutzername: admin   
- Passwort: 123456AD

**Mitarbeiter-Konto(User):**

- Benutzername: testuser  
- Passwort: save2log

Verwenden Sie diese Anmeldedaten, um die verschiedenen Rollen und Funktionen innerhalb der Anwendung zu testen.

# Django-Projekt mit Anaconda

Dieses Django-Projekt wurde mit Anaconda erstellt und enthält eine `requirements.txt`-Datei, die alle erforderlichen Pakete und Bibliotheken für das Projekt auflistet.

## Python-Installation

Stellen Sie sicher, dass Python auf Ihrem Computer installiert ist. Wenn nicht, befolgen Sie diese Schritte, um Python herunterzuladen und zu installieren:

1. Besuchen Sie die offizielle Python-Website ↗.
2. Laden Sie die neueste Python-Version für Ihr Betriebssystem herunter.
3. Öffnen Sie die Installationsdatei und folgen Sie den Anweisungen auf dem Bildschirm, um Python auf Ihrem System zu installieren. Stellen Sie sicher, dass Sie während der Installation die Option "Add Python to PATH" aktivieren.

## Installation von Anaconda

1. Laden Sie die Installationsdatei von der [Anaconda-Website](https://www.anaconda.com/products/distribution) herunter, die für Ihr Betriebssystem geeignet ist.
2. Öffnen Sie die Installationsdatei und folgen Sie den Anweisungen auf dem Bildschirm, um Anaconda auf Ihrem System zu installieren.


## Verwendung

Die Plattform FaceGate ermöglicht es den Nutzern, ihre beruflichen Informationen effizient zu verwalten. Die Interaktion mit der Anwendung variiert je nach Benutzerrolle: Mitarbeiter oder Administrator. Administratoren haben die Möglichkeit, Mitarbeiter hinzuzufügen, zu löschen oder deren Daten zu ändern sowie Abteilungen zu ergänzen, zu entfernen oder zu aktualisieren. Mitarbeiter hingegen können ihre Arbeitszeiten einsehen, Urlaub beantragen, Krankheitstage melden und entsprechende Bescheinigungen hochladen. Zusätzlich können sie Bilder für die Gesichtserkennung in Echtzeit aufnehmen für die Gesichtserkennung Prozess.

## Lizenz

Copyright (c) <2024> HTW Berlin Fachübergreifendesprojekt Gruppe 7 (Ines Bouazizi, Mohamed Boudinar, Lukas Wenzel)

Jedem, der eine Kopie dieser Software und der zugehörigen Dokumentationsdateien (die "Software") erhält, wird hiermit kostenlos die Erlaubnis erteilt, ohne Einschränkung mit der Software zu handeln, einschließlich und ohne Einschränkung der Rechte zur Nutzung, zum Kopieren, Ändern, Zusammenführen, Veröffentlichen, Verteilen, Unterlizenzieren und/oder Verkaufen von Kopien der Software, und Personen, denen die Software zur Verfügung gestellt wird, dies unter den folgenden Bedingungen zu gestatten:
Der obige Urheberrechtshinweis und dieser Genehmigungshinweis müssen in allen Kopien oder wesentlichen Teilen der Software enthalten sein.
DIE SOFTWARE WIRD OHNE MÄNGELGEWÄHR UND OHNE JEGLICHE AUSDRÜCKLICHE ODER STILLSCHWEIGENDE GEWÄHRLEISTUNG, EINSCHLIEßLICH ABER NICHT BESCHRÄNKT AUF DIE GEWÄHRLEISTUNG DER MARKTGÄNGIG-KEIT, DER EIGNUNG FÜR EINEN BESTIMMTEN ZWECK UND DER NICHTVERLET-ZUNG VON RECHTEN DRITTER, ZUR VERFÜGUNG GESTELLT. DIE AUTOREN ODER URHEBERRECHTSINHABER SIND IN KEINEM FALL HAFTBAR FÜR ANSPRÜCHE, SCHÄDEN ODER ANDERE VERPFLICHTUNGEN, OB IN EINER VERTRAGS- ODER HAFTUNGSKLAGE, EINER UNERLAUBTEN HANDLUNG ODER ANDERWEITIG, DIE SICH AUS, AUS ODER IN VERBINDUNG MIT DER SOFTWARE ODER DER NUTZUNG ODER ANDEREN GESCHÄFTEN MIT DER SOFTWARE ERGEBEN.
