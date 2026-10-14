# Hunar AI Advisor Recruitment Prototype

A Streamlit prototype for a Mumbai life-insurance advisor recruitment workflow. It supports Excel/CSV lead intake, consent-gated screening calls through the Hunar Voice API, retrieval of structured call results, candidate routing, a separate visit-scheduling agent workflow, and local workflow records.

## Features

- Upload and review candidate lead files (Excel/CSV).
- Require operator consent checks before initiating outbound calls.
- Initiate screening calls through the Hunar Voice API and retrieve call results.
- Review structured candidate responses and route follow-ups.
- Use a separate Visit-Scheduling Agent workflow for eligible candidates.
- Review scheduling outcomes before recording a local appointment entry.

## Requirements

- Python 3.10 or newer recommended.
- A Hunar Voice API key and authorization to use the relevant agents.
- Only approved leads with documented consent for live outreach.

## Run locally

1. Download or clone this repository.
2. Create and activate a virtual environment.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set your API key as an environment variable.

   **Windows PowerShell:**

   ```powershell
   $env:HUNAR_API_KEY="your_actual_api_key"
   ```

   **macOS/Linux:**

   ```bash
   export HUNAR_API_KEY="your_actual_api_key"
   ```

5. Start the app:

   ```bash
   streamlit run app.py
   ```

6. Open the local URL printed by Streamlit in your browser.

Do not put your real API key in source code, README files, screenshots, or GitHub commits. If a key has previously been exposed, rotate it before using the prototype.

## Important limitations and safe use

- This is a prototype, not a production recruitment system.
- Live calls can reach real people. Use only approved, consented leads and follow applicable calling windows and opt-out/do-not-contact requests.
- Review agent-extracted information before making recruitment decisions.
- Appointment entries in this prototype are local records; they do not confirm a booking in an external calendar or CRM.
- Local app data is excluded from this repository because it may contain candidate details or call history.
- Do not commit real candidate data, phone numbers, call recordings, API keys, or other personal information.

## Suggested demo flow

1. Upload a sample lead sheet.
2. Review the lead fields and consent status.
3. Demonstrate screening only with an explicitly approved test candidate.
4. Retrieve and review the completed call result.
5. Demonstrate the separate visit-scheduling workflow and human review.
6. Show the dashboard/workflow records and explain which records are live API results versus local/demo data.

## Configuration

The app uses the Hunar Voice API base URL and configured agent IDs in `app.py`. Confirm that the IDs and permissions are valid for your Hunar account before a demonstration. Do not make live calls to dummy phone numbers.
