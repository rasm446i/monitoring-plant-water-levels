class Microcontroller:
    def __init__(self, name, details, grafana_link):
        self.name = name
        self.details = details
        self.grafana_link = grafana_link


# Hardcoded embedded grafana links
microcontrollers = {
    '1': Microcontroller('Microcontroller 1', 'Denne plante er en philodendron',
                         'http://10.0.70.233:3000/d-solo/bb790f6a-28b1-445a-bd4b-fa33a881a9c8/microcontroller-1?orgId'
                         '=1&refresh=5s&from=1700713790081&to=1700735390081&theme=light&panelId=1'),
    '2': Microcontroller('Microcontroller 2', 'Denne plante er en philodendron',
                         'http://10.0.70.233:3000/d-solo/d97667fb-761b-42e2-a6de-badfbbc236f9/microcontroller-2?orgId'
                         '=1&refresh=5s&from=1700735143337&to=1700735443337&theme=light&panelId=1')
}
