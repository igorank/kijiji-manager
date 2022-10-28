from guerrillamail import GuerrillaMailSession


class GuerrillaMail:

    def __init__(self):
        self.session = GuerrillaMailSession()

    def get_email_add(self):
        return self.session.get_session_state()['email_address']

    def get_last_email_id(self):
        return self.session.get_email_list()[0].guid

    def get_email_body(self, email_id):
        return str(self.session.get_email(email_id).body)

    @staticmethod
    def get_inboxlv_code(email_body):
        index = email_body.find("</span>")
        return email_body[index - 6:index]