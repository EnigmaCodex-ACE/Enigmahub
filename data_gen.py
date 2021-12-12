from handledb import add_value_to_db

def data_gen():
    title = input("Enter title: ")
    team_mates_rno = input("Enter team mates roll no (CSV): ").split(',')
    team_mates_names = input("Enter team mates names (CSV): ").split(',')
    branch = input("Enter branch: ")
    github = input("Enter github link: ")
    youtube = input("Enter youtube link: ")
    abstract = input("Enter abstract: ")
    explainer = input("Enter explainer: ")
    footnote = input("Enter footnote: ")
    mentor = input("Enter mentor: ")
    links = input("Enter links (CSV): ").split(',')
    send_json = {
        "_id":team_mates_rno[0],
        "title":title,
        "team":team_mates_rno,
        "teamnames":team_mates_names,
        "github":github,
        "youtube":youtube,
        "abstract":abstract,
        "explainer":explainer,
        "footnote":footnote,
        "mentor":mentor,
        "leader":team_mates_names[0],
        "links":links,
        "branch":branch
    }
    print(send_json)
    add_value_to_db(send_json)

if(__name__ == "__main__"):
    data_gen()