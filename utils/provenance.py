# Utilities to identify the provencance of a notebook entry

from datetime import date

class Provenance:
    
    def __init__(self,
            name='User Name',
            email='user@domain.edu',
            tag='TAG',
            page='0000',
            title='Entry Title',
            date=str(date.today())
            ):
        
        self.name = name    # Full name of the notebook keeper (ex: John Doe)
        self.email = email  # User email
        self.tag = tag      # Tag to identify notebook keeper, usually initials (ex: JHD)
        self.date = date    # Date of the experiment yyyy-mm-dd, default is date of notebook creation (ex: 2023-06-22)
        self.page = page    # Page number, assuming 4-digit BPPP format (ex: 2034)
        self.title = title  # Descriptive title of notebook entry (ex: Hydrothermal Growth of YVO4 in HNO3/HCL)

    def header(self):

        # Prints a notebook header from provenance

        print(f"""
            {self.name}
            {self.email}
            {self.tag}
            {self.page}
            {self.title}
            {self.date}
            """
        )