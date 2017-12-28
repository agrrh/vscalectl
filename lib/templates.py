class Templates(object):
    def __init__(self):
        pass

    ACCOUNT = (
        "ID:\t{id}\n" +
        "Status:\t{status}\n" +
        "Name:\t{name}\n" +
        "Email:\t{email}\n" +
        "Phone:\t{phone}"
    )

    SERVERS_ONE = (
        "CTID:\t\t{ctid}\n" +
        "Status:\t\t{status}\n" +
        "Name:\t\t{name}\n" +
        "Hostname:\t{hostname}\n" +
        "Image:\t\t{image}\n" +
        "Address:\t{address}{address_private}\n" +
        "Keys:\t\t{keys}\n" +
        "Location:\t{location}\n" +
        "Plan:\t\t{plan}\n" +
        "Locked:\t\t{locked}"
    )

    SERVERS_ROW = "{ctid:<10}{locked}{status:<10}{name:<24}{address:<16}{plan:<8}{location:<8}{image:<24}"

    IMAGES_ROW = "{id:<32}{plans:<36}{locations:<24}"

    LOCATIONS_ROW = "{id:<6}{plans:<36}{description}"

    PLANS_ROW = "{id:<10}{price:<8}{cpus:<6}{ram:<6}{disk:<6}{ips:<4}{locations}"
