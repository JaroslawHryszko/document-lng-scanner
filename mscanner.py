import mailbox
import language_tool_python
import csv

email_address = ''
MBOX_file_path = ''

def load_emails_from_mbox(file_path):
    mbox = mailbox.mbox(file_path)
    emails = []
    for message in mbox:
        if message['from'] and email_address in message['from']:
            emails.append(message.get_payload(decode=True).decode('utf-8', errors='ignore'))
    return emails

def check_errors(text):
    tool = language_tool_python.LanguageTool('pl')  # 'pl' dla języka polskiego
    matches = tool.check(text)
    errors = [match.message for match in matches]
    return errors

emails = load_emails_from_mbox(MBOX_file_path)

for email in emails:
    errors = check_errors(email)
    if errors:
        print("Errors found in email:")
        for error in errors:
            print(error)

def save_errors_to_csv(errors_list, output_file='errors_report.csv'):
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Email Content', 'Error Message'])
        for email, errors in errors_list:
            for error in errors:
                writer.writerow([email, error])

errors_list = [(email, check_errors(email)) for email in emails]
save_errors_to_csv(errors_list)

