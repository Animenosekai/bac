# BUILD_NUMBER: 2
# BUILD_HASH: 3b2f8fdd02fc6e1f6d717f52b8863c3bd367236067590048e72409a10e43e03b
from io import BytesIO
import json
from datetime import datetime
from pathlib import Path
from typing import Union

from PyPDF2 import PageObject, PdfReader
from tqdm import tqdm


# BUILT: CLASS_DATA
CLASS_DATA = {'070838047JDA': 'Terminale Azur', '070435028GHA': 'Terminale Azur', '070819391BJA': 'Terminale Azur', '070345972HHA': 'Terminale Azur', '070821868GDA': 'Terminale Azur', '153055833HKA': 'Terminale Azur', '070830864JJA': 'Terminale Azur', '070835885BEA': 'Terminale Azur', '090823019CBA': 'Terminale Azur', '153094642HAA': 'Terminale Azur', '070825156HDA': 'Terminale Azur', '081451982JCA': 'Terminale Azur', '080629949EAA': 'Terminale Azur', '091022470ACA': 'Terminale Azur', '070821575GFA': 'Terminale Azur', '091125528FFA': 'Terminale Azur', '081619122HDA': 'Terminale Azur', '060407744HDA': 'Terminale Azur', '153098679BAA': 'Terminale Azur', '090952914AKA': 'Terminale Azur', '070835905KBA': 'Terminale Azur', '070826020JCA': 'Terminale Azur', '091143536JKA': 'Terminale Azur', '070836087AGA': 'Terminale Azur', '070407029DDA': 'Terminale Azur', '153031121FGA': 'Terminale Azur', '080789201GCA': 'Terminale Azur', '090851905EBA': 'Terminale Azur', '070831220CDA': 'Terminale Corail', '070840666JDA': 'Terminale Corail', '070301583EAA': 'Terminale Corail', '153098673BGA': 'Terminale Corail', '070819982AKA': 'Terminale Corail', '110857316AHA': 'Terminale Corail', '153051635AKA': 'Terminale Corail', '070836417GEA': 'Terminale Corail', '070820228FEA': 'Terminale Corail', '153065229KCA': 'Terminale Corail', '101060979CDA': 'Terminale Corail', '070823400JDA': 'Terminale Corail', '130903483FEA': 'Terminale Corail', '153054062AHA': 'Terminale Corail', '070838631JBA': 'Terminale Corail', '101138686BDA': 'Terminale Corail', '100393665HEA': 'Terminale Corail', '070824452ABA': 'Terminale Corail', '110828516KFA': 'Terminale Corail', '153060367AHA': 'Terminale Corail', '090854315FGA': 'Terminale Corail', '153092489JKA': 'Terminale Corail', '100333449FDA': 'Terminale Corail', '091129156BGA': 'Terminale Corail', '153093804DFA': 'Terminale Corail', '153059665DAA': 'Terminale Corail', '070826696JFA': 'Terminale Corail', '101030538AGA': 'Terminale Corail', '101145092AKA': 'Terminale Corail', '091132961KBA': 'Terminale Emeraude', '070824651KDA': 'Terminale Emeraude', '091129150CCA': 'Terminale Emeraude', '100836619CCA': 'Terminale Emeraude', '070837377HEA': 'Terminale Emeraude', '153093332CCA': 'Terminale Emeraude', '071137907FAA': 'Terminale Emeraude', '070836044EKA': 'Terminale Emeraude', '060373490JGA': 'Terminale Emeraude', '081582201DHA': 'Terminale Emeraude', '060396228EGA': 'Terminale Emeraude', '090224161ABA': 'Terminale Emeraude', '080245514GEA': 'Terminale Emeraude', '070826025HHA': 'Terminale Emeraude', '111003659DHA': 'Terminale Emeraude', '070833532DKA': 'Terminale Emeraude', '070829610JBA': 'Terminale Emeraude', '060374986EFA': 'Terminale Emeraude', '070829025JEA': 'Terminale Emeraude', '153092524FEA': 'Terminale Emeraude', '153092502HGA': 'Terminale Emeraude', '060351227DKA': 'Terminale Emeraude', '091131501KGA': 'Terminale Emeraude', '070829930FCA': 'Terminale Emeraude', '080787907KFA': 'Terminale Emeraude', '070826816GCA': 'Terminale Emeraude', '070835309AJA': 'Terminale Emeraude', '060408318JBA': 'Terminale Indigo', '091126244BJA': 'Terminale Indigo', '153093310EEA': 'Terminale Indigo', '070834136BHA': 'Terminale Indigo', '081227366EGA': 'Terminale Indigo', '071553782BEA': 'Terminale Indigo', '071702706JCA': 'Terminale Indigo', '110955175CBA': 'Terminale Indigo', '080788740DJA': 'Terminale Indigo', '153093295FKA': 'Terminale Indigo', '110955176CAA': 'Terminale Indigo', '153092526FCA': 'Terminale Indigo', '101008264GHA': 'Terminale Indigo', '153101592AHA': 'Terminale Indigo', '070829697KBA': 'Terminale Indigo', '153092512GGA': 'Terminale Indigo', '070839788JJA': 'Terminale Indigo', '070823397JGA': 'Terminale Indigo', '070218750DFA': 'Terminale Indigo', '070822358FJA': 'Terminale Indigo', '153065368FAA': 'Terminale Indigo', '070830392HFA': 'Terminale Indigo', '153091650FFA': 'Terminale Indigo', '080228408ABA': 'Terminale Indigo', '193040113HCA': 'Terminale Indigo', '070836478ADA': 'Terminale Indigo', '153092505HDA': 'Terminale Indigo', '070831766FKA': 'Terminale Indigo', '153093385GGA': 'Terminale Indigo', '070624138BAA': 'Terminale Indigo', '070824616DBA': 'Terminale Lilas', '101060989BDA': 'Terminale Lilas', '070825956EKA': 'Terminale Lilas', '110955171CFA': 'Terminale Lilas', '101060993AKA': 'Terminale Lilas', '153086557AHA': 'Terminale Lilas', '091126240CCA': 'Terminale Lilas', '153096672HHA': 'Terminale Lilas', '153102525EEA': 'Terminale Lilas', '070822319KHA': 'Terminale Lilas', '153102523EGA': 'Terminale Lilas', '070832958DBA': 'Terminale Lilas', '070833903FGA': 'Terminale Lilas', '091129171ABA': 'Terminale Lilas', '153028786GDA': 'Terminale Lilas', '101138669DAA': 'Terminale Lilas', '070840081JGA': 'Terminale Lilas', '060424766CGA': 'Terminale Lilas', '101138675CEA': 'Terminale Lilas', '070819412KEA': 'Terminale Lilas', '070831958GBA': 'Terminale Lilas', '070836052EBA': 'Terminale Lilas', '072212730JEA': 'Terminale Lilas', '070820438DJA': 'Terminale Lilas', '070831176GHA': 'Terminale Lilas', '080815879FKA': 'Terminale Lilas', '110857331JKA': 'Terminale Lilas', '070836803GGA': 'Terminale Lilas', '110955180BGA': 'Terminale Lilas', '070833238ECA': 'Terminale Turquoise', '081204326KHA': 'Terminale Turquoise', '070821890EBA': 'Terminale Turquoise', '100978746KHA': 'Terminale Turquoise', '110861809HDA': 'Terminale Turquoise', '070820682JFA': 'Terminale Turquoise', '070834115DJA': 'Terminale Turquoise', '070820321FJA': 'Terminale Turquoise', '153093311EDA': 'Terminale Turquoise', '153035594EFA': 'Terminale Turquoise', '153087125CBA': 'Terminale Turquoise', '070819629HBA': 'Terminale Turquoise', '070819650FAA': 'Terminale Turquoise', '070835774CJA': 'Terminale Turquoise', '110567842DDA': 'Terminale Turquoise', '153062396BFA': 'Terminale Turquoise', '153092579KGA': 'Terminale Turquoise', '070124411KAA': 'Terminale Turquoise', '091129188JBA': 'Terminale Turquoise', '070818311DBA': 'Terminale Turquoise', '060422227EDA': 'Terminale Turquoise', '070819254FJA': 'Terminale Turquoise', '120738388DEA': 'Terminale Turquoise', '070830600GBA': 'Terminale Turquoise', '080787932HAA': 'Terminale Turquoise', '080778562DBA': 'Terminale Turquoise', '070824996DKA': 'Terminale Turquoise', '153451034FGA': 'Terminale Turquoise'}


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
