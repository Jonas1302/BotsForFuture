import logging
import re
from bff.api import User, respond_to

logger = logging.getLogger(__name__)

valid_mobile_phone_number = re.compile("^(0|(\\+49( )?)|(0049( )?))1[0-9 ]+$")


class VCF:
    def __init__(self):
        self.string = "BEGIN:VCARD\n"
    
    def finalize(self):
        # check if `next_contact` was the latest method called
        # in this case we simply remove the beginning of the new contact (which is currently empty)
        if self.string.endswith("\nBEGIN:VCARD\n"):
            return self.string.rsplit("\nBEGIN:VCARD\n", 1)[0]
        
        assert self.n and self.fn
        return self.string + "END:VCARD"
    
    def next_contact(self):
        assert self.n and self.fn
        self.string += "END:VCARD\nBEGIN:VCARD\n"
        self.fn = False
        self.n = False
    
    def add_display_name(self, display_name):
        self.string += f"FN:{display_name}\n"
        self.fn = True
    
    def add_name(self, forename, surname=None):
        self.string += f"N:{surname if surname else ''};{forename};;;\n"
        self.n = True
    
    def add_email(self, email):
        self.string += f"EMAIL:{email}\n"
    
    def add_phone(self, number, type_=None):
        if type_:
            self.string += f"TEL;TYPE={type_}:{number}\n"
        else:
            self.string += f"TEL:{number}\n"


@respond_to("vcf ([\S]*)")
@respond_to("contacts ([\S]*)")
def get_vcf(message):
    # TODO insert suffix
    users = User.get_users()
    vcf = VCF()
    
    for user in users:
        if not user.position:
            logger.info(f"{user.name} has not provided a phone number")
            continue
        
        if not valid_mobile_phone_number.match(user.position):
            logger.info(f"{user.name} had an invalid phone number: {user.position}")
            continue
        
        vcf.add_display_name(user.name)
        
        if user.first_name:
            vcf.add_name(user.first_name, user.last_name)
        else:
            vcf.add_name(user.name)
        
        if user.email:
            vcf.add_email(user.email)
        
        vcf.add_phone(user.position, "CELL")
        vcf.next_contact()
    
    return vcf.finalize()
