from io import BytesIO
import json
from datetime import datetime
from pathlib import Path
from typing import Union

from PyPDF2 import PageObject, PdfReader
from tqdm import tqdm


with open("data/class.json") as f:  # BUILD: CLASS_DATA
    CLASS_DATA = json.load(f)  # BUILD: CLASS_DATA


def trim_to_next_number(string: str):
    string = str(string)
    for l in string:
        if l.isnumeric():
            break
        string = string[1:]
    return string


class Gender:
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"


class Birthplace:
    def __init__(self, data: str) -> None:
        self.raw = str(data).strip()
        self.city, _, editing = self.raw.partition("(")
        self.city = self.city.strip().title()
        dpt, _, _ = editing.partition(")")
        self.country = "France"
        if dpt.isnumeric():
            self.foreign = False
            self.department = int(dpt)
        else:
            self.foreign = True
            self.department = None
            self.country = dpt.title()

    def __repr__(self) -> str:
        return "Birthplace({place})".format(place=self.raw)

    def as_dict(self, camelCase: bool = False):
        return {
            "department": self.department,
            "city": self.city,
            "country": self.country,
            "foreign": self.foreign
        }


class Address:
    def __init__(self, data: str) -> None:
        self.raw = str(data).strip()
        try:
            self.postal_code, _, self.city = self.raw.splitlines()[-1].partition(" ")
            self.postal_code = int(self.postal_code.strip())
            self.city = self.city.strip().title()
        except Exception:
            try:
                self.postal_code
            except Exception:
                self.postal_code = None
            try:
                self.city
            except Exception:
                self.city = None

    def __repr__(self) -> str:
        return "Address({address})".format(address=self.raw.splitlines()[0])

    def as_dict(self, camelCase: bool = False):
        results = {
            "raw": self.raw,
            "postal_code": self.postal_code,
            "city": self.city
        }
        if camelCase:
            results["postalCode"] = results.pop("postal_code")
        return results


class Grade:
    def __init__(self, data: str) -> None:
        self.raw = str(data).strip()
        editing = self.raw

        major, _, after = editing.partition(".")
        self.coefficient = float(major + "." + after[:2])
        editing = after[2:]

        major, _, after = editing.partition(".")
        self.grade = float(major + "." + after[:2])
        editing = after[2:]

        major, _, after = editing.partition(".")
        self.points = float(major + "." + after[:2])

    def __repr__(self) -> str:
        return "Grade(coefficient={coefficient}, grade={grade}, points={points})".format(coefficient=self.coefficient, grade=self.grade, points=self.points)

    def as_dict(self, camelCase: bool = False):
        return {
            "coefficient": self.coefficient,
            "grade": self.grade,
            "points": self.points
        }


class GradeWithName(Grade):
    def __init__(self, data: str, name: str) -> None:
        super().__init__(data)
        self.name = str(name).strip()

    def as_dict(self, camelCase: bool = False):
        results = super().as_dict(camelCase)
        results["name"] = self.name
        return results


class Total:
    def __init__(self, data: str, alternative: bool = False) -> None:
        self.raw = str(data).strip()
        editing = self.raw

        if not alternative:
            major, _, after = editing.partition(".")
            # print(major, ".", after)
            self.coefficient = float(major + "." + after[:1])
            editing = after[1:]

            major, _, after = editing.partition(".")
            self.points = float(major + "." + after[:2])
        else:
            _, _, editing = editing.partition(":")
            grade, _, editing = editing.partition("Total")
            self.coefficient = float(grade.strip())

            _, _, editing = editing.partition(":")
            grade, _, editing = editing.partition("\n")
            self.points = float(grade.strip())

    def __repr__(self) -> str:
        return "Total(coefficient={coefficient}, points={points})".format(coefficient=self.coefficient, points=self.points)

    def as_dict(self, camelCase: bool = False):
        return {
            "coefficient": self.coefficient,
            "points": self.points
        }


class Epreuves:
    def __init__(self, data: str) -> None:
        self.raw = str(data).strip()
        editing = self.raw

        _, _, editing = editing.partition("Français")

        _, _, editing = editing.partition("A01 2021")
        grades, _, editing = editing.partition("\n")
        self.french_written = Grade(grades) if not "Dispensé" in grades else None
        # print("french written:", self.french_written)

        _, _, editing = editing.partition("A01 2021")
        grades, _, editing = editing.partition("\n")
        self.french_speaking = Grade(grades) if not "Dispensé" in grades else None
        # print("french speaking:", self.french_speaking)

        editing = trim_to_next_number(editing)
        grades, _, editing = editing.partition("\n")
        self.philosophy = Grade(grades) if not "Dispensé" in grades else None
        # print("philosophy:", self.philosophy)

        editing = trim_to_next_number(editing)
        grades, _, editing = editing.partition("\n")
        self.grand_oral = Grade(grades) if not "Dispensé" in grades else None
        # print("grand oral:", self.grand_oral)

        grades, _, editing = editing.partition("\n")
        name, _, grades = grades.rpartition(" ")
        name = name.replace("\n", " ").strip()
        self.options = [name.strip()]
        self.first_option = GradeWithName(grades, name) if not "Dispensé" in grades else None
        # print("first option:", self.first_option)

        grades, _, editing = editing.partition("\n")
        name, _, grades = grades.rpartition(" ")
        name = name.replace("\n", " ").strip()
        self.options.append(name.strip())
        self.second_option = GradeWithName(grades, name) if not "Dispensé" in grades else None
        # print("second option:", self.second_option)
        # print("options:", self.options)

        self.total = Total(editing.rpartition(" ")[2])
        # print("total:", self.total)

        # input("\n\nEditing\n-------\n" + editing + "\n[enter] to continue...")

    def __repr__(self) -> str:
        return "Epreuves({total})".format(self.total)

    def as_dict(self, camelCase: bool = False):
        results = {
            "french_written": self.french_written.as_dict(camelCase),
            "french_speaking": self.french_speaking.as_dict(camelCase),
            "philosophy": self.philosophy.as_dict(camelCase),
            "grand_oral": self.grand_oral.as_dict(camelCase),
            "first_option": self.first_option.as_dict(camelCase),
            "second_option": self.second_option.as_dict(camelCase),
            "options": self.options,
            "total": self.total.as_dict(camelCase)
        }
        if camelCase:
            results["frenchWritten"] = results.pop("french_written")
            results["frenchSpeaking"] = results.pop("french_speaking")
            results["grandOral"] = results.pop("grand_oral")
            results["firstOption"] = results.pop("first_option")
            results["secondOption"] = results.pop("second_option")
        return results


class Premiere:
    history: Grade = None
    ensc: Grade = None
    first_language: GradeWithName = None
    second_language: GradeWithName = None
    option: GradeWithName = None
    all: Grade = None

    def as_dict(self, camelCase: bool = False):
        results = {
            "history": self.history.as_dict(camelCase) if self.history is not None else None,
            "first_language": self.first_language.as_dict(camelCase) if self.first_language is not None else None,
            "second_language": self.second_language.as_dict(camelCase) if self.second_language is not None else None,
            "ensc": self.ensc.as_dict(camelCase) if self.ensc is not None else None,
            "option": self.option.as_dict(camelCase) if self.option is not None else None,
            "all": self.all.as_dict(camelCase if self.all is not None else None)
        }
        if camelCase:
            results["firstLanguage"] = results.pop("first_language")
            results["secondLanguage"] = results.pop("second_language")
        return results


class Terminale:
    history: Grade = None
    emc: Grade = None
    first_language: GradeWithName = None
    second_language: GradeWithName = None
    ensc: Grade = None
    sport: Grade = None

    def as_dict(self, camelCase: bool = False):
        results = {
            "history": self.history.as_dict(camelCase) if self.history is not None else None,
            "emc": self.emc.as_dict(camelCase) if self.emc is not None else None,
            "first_language": self.first_language.as_dict(camelCase) if self.first_language is not None else None,
            "second_language": self.second_language.as_dict(camelCase) if self.second_language is not None else None,
            "ensc": self.ensc.as_dict(camelCase) if self.ensc is not None else None,
            "sport": self.sport.as_dict(camelCase) if self.sport is not None else None
        }
        if camelCase:
            results["firstLanguage"] = results.pop("first_language")
            results["secondLanguage"] = results.pop("second_language")
        return results


class ControleContinu:
    def __init__(self, data: str) -> None:
        self.premiere = Premiere()
        self.terminale = Terminale()
        self.raw = str(data).strip()
        editing = self.raw

        _, _, editing = editing.partition("Géographie")
        grades, _, editing = editing.partition("\n")
        self.premiere.history, self.terminale.history = self.split_two_grades(grades)
        # print("premiere history:", self.premiere.history)
        # print("terminale history:", self.terminale.history)

        _, _, editing = editing.partition("civique")
        grades, _, editing = editing.partition("\n")
        self.terminale.emc = Grade(grades) if not "Dispensé" in grades else None
        # print("terminale emc:", self.terminale.emc)

        for index, char in enumerate(editing):
            if char.isnumeric():
                break
        name = editing[:index]
        self.first_language = name[name.find("(") + 1:name.rfind(")")]

        editing = editing[index + 1:]
        grades, _, editing = editing.partition("\n")
        self.premiere.first_language, self.terminale.first_language = self.split_two_grades_with_name(grades, self.first_language)
        # print("first language:", self.first_language)
        # print("premiere first language:", self.premiere.first_language)
        # print("terminale first language:", self.terminale.first_language)

        for index, char in enumerate(editing):
            if char.isnumeric():
                break
        name = editing[:index]
        self.second_language = name[name.find("(") + 1:name.rfind(")")]

        editing = editing[index + 1:]
        grades, _, editing = editing.partition("\n")
        self.premiere.second_language, self.terminale.second_language = self.split_two_grades_with_name(grades, self.second_language)
        # print("second language:", self.second_language)
        # print("premiere second language:", self.premiere.second_language)
        # print("terminale second language:", self.terminale.second_language)

        _, _, editing = editing.partition("scientifique")
        grades, _, editing = editing.partition("\n")
        self.premiere.ensc, self.terminale.ensc = self.split_two_grades(grades)
        # print("premiere ensc:", self.premiere.ensc)
        # print("terminale ensc:", self.terminale.ensc)

        _, _, editing = editing.partition("sportive")
        grades, _, editing = editing.partition("\n")
        self.terminale.sport = Grade(grades) if not "Dispensé" in grades else None
        # print("terminale sport:", self.terminale.sport)

        for index, char in enumerate(editing):
            if char.isnumeric():
                break
        name = editing[:index]
        name = name.replace("\n", " ").strip()
        self.option_name = name
        editing = editing[index:]
        # print("option name:", self.option_name)

        grades, _, editing = editing.partition("\n")
        self.premiere.option = GradeWithName(grades.replace("(A01 2021)", "").replace(" ", ""), self.option_name)
        # print("premiere option:", self.premiere.option)

        _, _, editing = editing.partition("enseignements")
        grades, _, editing = editing.partition("\n")
        self.premiere.all = Grade(grades.replace("(A01 2021)", "").replace(" ", ""))
        # print("premiere all:", self.premiere.all)

        self.total = Total(editing, alternative=True)
        # print("total:", self.total)

        # input("\n\nEditing\n-------\n" + editing + "\n[enter] to continue...")

    def split_two_grades(self, data: str):
        editing = data
        pos1 = editing.find(".") + 1
        editing = editing[pos1:]

        pos2 = editing.find(".") + 1
        editing = editing[pos2:]

        pos3 = editing.find(".") + 2
        second = editing[pos3:].replace("(A01 2021)", "")
        first = data[:pos1 + pos2 + pos3].replace("(A01 2021)", "")

        return Grade(first), Grade(second)

    def split_two_grades_with_name(self, data: str, name: str):
        a, b = self.split_two_grades(data)
        return GradeWithName(a.raw, name), GradeWithName(b.raw, name)

    def __repr__(self) -> str:
        return "ControleContinu({total})".format(self.total)

    def as_dict(self, camelCase: bool = False):
        results = {
            "option_name": self.option_name,
            "first_language": self.first_language,
            "second_language": self.second_language,

            "premiere": self.premiere.as_dict(camelCase),
            "terminale": self.terminale.as_dict(camelCase),

            "total": self.total.as_dict(camelCase)
        }
        if camelCase:
            results["optionName"] = results.pop("option_name")
            results["firstLanguage"] = results.pop("first_language")
            results["secondLanguage"] = results.pop("second_language")
        return results


class Optionnel:
    def __init__(self, data: str = "") -> None:
        self.raw = str(data).strip()
        editing = self.raw

        self.options = []
        self.first_option = None
        self.second_option = None
        self.third_option = None
        self.total = Total("0.00.00")

        if len(data) > 0:
            lines = editing.splitlines()
            total = lines.pop()
            # _, _, after = total.partition(":")
            # coeff, _, after = total.partition("Total")
            # _, _, points = total.partition(":")
            # self.total = Total()
            self.total = Total(total, alternative=True)
            for option in ["first_option", "second_option", "third_option"]:
                if len(lines) > 0:
                    line = lines.pop(0)
                    name, _, grades = line.rpartition(" ")
                    self.options.append(name.strip())
                    self.__setattr__(option, GradeWithName(grades, name))
                else:
                    break

            # input("\n\nEditing\n-------\n" + editing + "\n[enter] to continue...")

    def __repr__(self) -> str:
        return "Optionnel(options={options})".format(options=", ".join(self.options))

    def as_dict(self, camelCase: bool = False):
        results = {
            "options": self.options,
            "first_option": self.first_option.as_dict(camelCase) if self.first_option else None,
            "second_option": self.second_option.as_dict(camelCase) if self.second_option else None,
            "third_option": self.third_option.as_dict(camelCase) if self.third_option else None,
        }
        if camelCase:
            results["firstOption"] = results.pop("first_option")
            results["secondOption"] = results.pop("second_option")
            results["thirdOption"] = results.pop("third_option")
        return results


class CalculResultat:
    def __init__(self, data: str) -> None:
        self.raw = str(data).strip()
        editing = self.raw

        _, _, editing = editing.partition("terminales")
        grades, _, editing = editing.partition("\n")
        self.epreuves = Total(grades)
        # print("epreuves:", self.epreuves)

        _, _, editing = editing.partition("continu")
        grades, _, editing = editing.partition("\n")
        self.controle_continu = Total(grades)
        # print("controle continu:", self.controle_continu)

        if "Optionnel" in editing:
            _, _, editing = editing.partition("Optionnel(s)")
            grades, _, editing = editing.partition("\n")
            self.optionnel = Total(grades)
            # print("optionnel:", self.optionnel)
        else:
            self.optionnel = Total(("0.00.0"))

        if "Jury" in editing:
            _, _, editing = editing.partition("groupe")
            grades, _, editing = editing.partition("\n")
            self.jury = Total(("1.0" + grades).replace(" ", ""))
        else:
            self.jury = Total(("0.00.0"))

        _, _, editing = editing.partition("Totaux")
        grades, _, editing = editing.partition("\n")
        self.total = Total(grades)
        # print("total:", self.total)

        editing = trim_to_next_number(editing)
        self.average = float(editing.strip())
        # print("average:", self.average)

        # input("\n\nEditing\n-------\n" + editing + "\n[enter] to continue...")

    def __repr__(self) -> str:
        return "CalculResultat(average={average}, total={total})".format(average=self.average, total=self.total)

    def as_dict(self, camelCase: bool = False):
        results = {
            "epreuves": self.epreuves.as_dict(camelCase),
            "controle_continu": self.controle_continu.as_dict(camelCase),
            "optionnel": self.optionnel.as_dict(camelCase) if self.optionnel else None,
            "jury": self.jury.as_dict(camelCase) if self.jury else None,
            "total": self.total.as_dict(camelCase),
            "average": self.average
        }
        if camelCase:
            results["controleContinu"] = results.pop("controle_continu")
        return results


class Page:
    def __init__(self, page: PageObject) -> None:
        # print("\n\n\nNEXT\n")

        self.raw = page.extract_text()
        editing = self.raw

        self.academy, _, editing = editing.partition("Relevé des notes")
        self.academy = self.academy.replace("\n", " ")
        # print("academy:", self.academy)

        _, _, editing = editing.partition("session")
        self.session = int(editing[:editing.find("N")].strip())
        # print("session:", self.session)

        _, _, editing = editing.partition(":")
        self.candidate_number = int(editing[:editing.find("\n")].strip())
        # print("candidate number:", self.candidate_number)

        _, _, editing = editing.partition(":")
        self.registration_number = int(editing[:editing.find("\n")].strip())
        # print("registration number:", self.registration_number)

        if "Nom d'usage" in editing:
            _, _, editing = editing.partition(":")
            self.usage_name = editing[:editing.find("\n")].strip()
            # print("usage name:", self.usage_name)
        else:
            self.usage_name = None

        _, _, editing = editing.partition(":")
        self.first_names = editing[:editing.find("\n")].strip().split(" ")
        # print("first names:", self.first_names)

        _, _, editing = editing.partition(":")
        self.birthday = datetime.strptime(editing[:editing.find("\n")].strip(), "%d/%m/%Y")
        # print("birthday:", self.birthday)

        _, _, editing = editing.partition(":")
        self.ine, _, editing = editing.partition(":")
        self.ine = self.ine.strip()
        # print("INE:", self.ine)

        self.birthplace, _, editing = editing.partition("Nom")
        self.birthplace = Birthplace(self.birthplace)
        # print("birthplace:", self.birthplace)

        _, _, editing = editing.partition(":")[2].partition(":")
        editing = editing.lstrip()
        if editing.startswith("MONSIEUR"):
            self.gender = Gender.MALE
        elif editing.startswith("MADAME"):
            self.gender = Gender.FEMALE
        else:
            self.gender = Gender.OTHER
        # print("gender:", self.gender)

        _, _, editing = editing.partition(" ")
        splitted = editing.split()
        results = []
        for word in splitted:
            if not all(c.isupper() for c in word if c.isalpha()):
                break
            results.append(word)
        self.last_name = " ".join(results)
        # print("last name:", self.last_name)

        editing = trim_to_next_number(editing)

        self.address, _, editing = editing.partition("\n\n")
        self.address = Address(self.address)
        # print("address:", self.address)

        _, _, editing = editing.partition("\n")

        editing = trim_to_next_number(editing)
        self.school_id, _, editing = editing.partition(" ")
        self.school_id = self.school_id.strip()
        # print("school id:", self.school_id)

        self.school, _, editing = editing.partition("Etablissement")
        self.school = self.school.strip()
        # print("school:", self.school)

        editing = trim_to_next_number(editing)
        self.jury, _, editing = editing.partition("\n")
        self.jury = int(self.jury.strip())
        # print("jury:", self.jury)

        self.epreuves, _, editing = editing.partition("Contrôle continu")
        self.epreuves = Epreuves(self.epreuves)

        controle_continu, _, editing = editing.partition("Calcul résultat")
        self.controle_continu = ControleContinu(controle_continu)

        if "Optionnel" in controle_continu:
            _, _, controle_continu = controle_continu.partition("Optionnel")
            _, _, controle_continu = controle_continu.partition("Points")
            self.optionnel = Optionnel(controle_continu)
        else:
            self.optionnel = Optionnel()

        self.calcul_resultat, _, editing = editing.partition("\n\n")
        self.calcul_resultat = CalculResultat(self.calcul_resultat)

        # SKIPPING SIGN ?
        _, _, editing = editing.partition("\n\n")

        if "Mention" in editing:
            _, _, editing = editing.partition("Mention")
            self.mention, _, editing = editing.partition("\n")
            self.mention = self.mention.strip()
        else:
            self.mention = None
        # print("mention:", self.mention)

        self.class_name = CLASS_DATA.get(self.ine, "Autre")

        # input("\n\nEditing\n-------\n" + editing + "\n[enter] to continue...")

        # # print(self.first_names, self.last_name)

    def as_dict(self, camelCase: bool = False):
        results = {
            "academy": self.academy,
            "session": self.session,
            "candidate_number": self.candidate_number,
            "registration_number": self.registration_number,
            "first_names": self.first_names,
            "last_name": self.last_name,
            "usage_name": self.usage_name,
            "birthday": self.birthday.isoformat(),
            "birthday_timestamp": int(self.birthday.timestamp()),
            "ine": self.ine,
            "birthplace": self.birthplace.as_dict(camelCase),
            "gender": self.gender,
            "address": self.address.as_dict(camelCase),
            "school": self.school,
            "school_id": self.school_id,
            "jury": self.jury,
            "epreuves": self.epreuves.as_dict(camelCase),
            "controle_continu": self.controle_continu.as_dict(camelCase),
            "optionnel": self.optionnel.as_dict(camelCase) if self.optionnel else None,
            "calcul_resultat": self.calcul_resultat.as_dict(camelCase),
            "mention": self.mention,
            "class": self.class_name
        }
        if camelCase:
            results["candidateNumber"] = results.pop("candidate_number")
            results["registrationNumber"] = results.pop("registration_number")
            results["firstNames"] = results.pop("first_names")
            results["lastName"] = results.pop("last_name")
            results["usageName"] = results.pop("usage_name")
            results["birthdayTimestamp"] = results.pop("birthday_timestamp")
            results["schoolID"] = results.pop("school_id")
            results["controleContinu"] = results.pop("controle_continu")
            results["calculResultat"] = results.pop("calcul_resultat")
        return results


class Document:
    def __init__(self, file: Union[str, Path, BytesIO]) -> None:
        self.reader = PdfReader(file)
        self.pages: list[Page] = []
        print("Number of pages:", len(self.reader.pages) // 2)
        for i in tqdm(range(0, len(self.reader.pages), 2), desc="Extracting data", unit="page"):
            # print("Current page:", i, end="\r")
            self.pages.append(Page(self.reader.pages[i]))
