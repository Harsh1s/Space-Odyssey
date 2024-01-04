from firebase_admin import credentials, db, initialize_app
from os.path import dirname
from miscellaneous import hasher

config = {
    "database": {
        "firebaseDB": "https://stellar-ff50f-default-rtdb.asia-southeast1.firebasedatabase.app/",
        "firebaseStorage": "stellar-ff50f.appspot.com",
    }
}

# Initialize Firebase app
cred = credentials.Certificate(
    dirname(__file__) + "/" + "./credentials-space-odyssey.json"
)
initialize_app(
    cred,
    {
        "databaseURL": config["database"]["firebaseDB"],
        "storageBucket": config["database"]["firebaseStorage"],
    },
)

ref = db.reference("space-odessey")
users_ref = ref.child("users")


def initialize_firebase_for_a_user(data: dict):
    """
    data["Name"] = request.form["Name"]
    data["Regno"] = request.form["Regno"].upper()
    data["Email"] = request.form["Email"]
    data["Password"] = sha256(request.form["Password"]).hexdigest()
    data["Phone"] = request.form["Phone"]
    data["ReceiptNo"] = request.form["ReceiptNo"]
    data["UniqID"] = generate_uuid()
    """
    if "uniqid" in data:
        reg_number_ref = users_ref.child(data["regno"].casefold())
        selector = reg_number_ref.get()
        if selector:
            if "name" in selector:
                print(f"user {data['regno']} already exists")
        else:
            if "points" not in data:
                data["points"] = 0
            reg_number_ref.update(data)
    else:
        print("uniq id not present")


def get_team_dict(regno: str):
    regno = regno.casefold()
    reg_number_ref = users_ref.child(regno)
    selector = reg_number_ref.get()
    if selector:
        return selector
    else:
        return None


def get_team_details(regno: str, field_name: str, default_if_not_exist=None):
    regno = regno.casefold()
    reg_number_ref = users_ref.child(regno)
    selector = reg_number_ref.get()
    if selector:
        if field_name in selector:
            return selector[field_name]
        else:
            if default_if_not_exist:
                update_team_details(regno, field_name, default_if_not_exist)
            return None
    else:
        return None


def update_team_details(regno: str, field_name: str, field_value):
    regno = regno.casefold()
    reg_number_ref = users_ref.child(regno)
    selector = reg_number_ref.get()
    if not selector:
        selector = dict()
    selector[field_name] = field_value
    selector_update = reg_number_ref
    selector_update.update(selector)


def check_password(regno: str, hashed_pw: str) -> bool:
    pw_on_firebase = get_team_details(regno, "password")
    if pw_on_firebase:
        if hashed_pw.casefold() == pw_on_firebase.casefold():
            return True
    return False


def get_current_question_from_firebase(regno: str) -> int:
    return int(get_team_details(regno, "current_question"))


def update_current_question_to_firebase(regno: str, question_number: int) -> None:
    update_team_details(regno, "current_question", int(question_number))


def get_points(regno: str) -> int:
    return int(get_team_details(regno, "points"))


def set_points(regno: str, points: int = 0):
    regno = regno.casefold()
    reg_number_ref = users_ref.child(regno)
    selector = reg_number_ref.get()
    if not selector:
        selector = dict()
    selector["points"] = points
    selector_update = reg_number_ref
    selector_update.update(selector)
    print(f"User {regno} has {points} points now")


def add_points(regno: str, points: int = 0):
    set_points(regno, get_points(regno) + int(points))


def get_ordered_list_of_users_based_on_points() -> list[tuple[str, str]]:
    # Returns a largest to smallest list of user based on their points. Format is [('Vishal N - 20BCE1043', '332'), ('dasdas - 20BCE1302', '213'), ('dasdad - 20B3231312', '132'), ('fasdas - 20BCE13231312', '13')]
    all_users_ref = users_ref.get()
    users_and_points = {
        all_users_ref[user]["name"]
        + " - "
        + user.upper(): all_users_ref[user]["current_question"]
        for user in all_users_ref
        if user
        and "current_question" in all_users_ref[user]
        and "name" in all_users_ref[user]
    }
    sorted_users_and_points = sorted(
        users_and_points.items(), key=lambda x: x[1], reverse=True
    )

    return sorted_users_and_points
