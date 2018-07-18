import os.path as path
import inspect

import FIOS.sample as sample

# files_dict = to_single_list(list(files.values()))
red2 = sample.font.red2
end = sample.font.end
d = sample.datetime

kinds_dict = {
    lambda x, n: Flag.create(x, n): lambda x: isinstance(x, (bool, type(None))),
    lambda x, n: Number.create(int(x) if isinstance(x, str) else x, n): lambda x: isinstance(x, (int, float, complex)) or str(x).isdigit(),
    lambda x, n: DataStructure.create(x, n): lambda x: isinstance(x, (list, tuple, dict, set, frozenset)),
    lambda x, n: TimeData.create(x, n): lambda x: isinstance(x, (d.date, d.time, d.datetime)),
    lambda x, n: Path.create(x, n): lambda x: path.isabs(str(x)),
    lambda x, n: String.create(x, n): lambda x: isinstance(x, str),
    lambda x, n: Substance.create(x, n): True
}


class Substance(object):
    def __init__(self, content, name=''):
        self.content = content
        self.name = str(inspect.stack()[5][4][0]).lstrip().split(" = ")[0] if not name else name
        self.kind = str(inspect.stack()[3][4][0][17::]).split('.')[0]
        self.kind = self.kind[0].lower() + self.kind[1:]
        self.type = abs(self)
        self.sign = sample.objects.get(self.kind)
        self.property = + self

    def __abs__(self):
        return str(type(self.content)).split("'")[1]

    # TODO: Overload
    def __str__(self):
        header = "Kind: {0}{2}{1}, Type: {0}{3}{1}, Property: {0}{4}{1}".format(red2, end, self.kind, self.type, self.property)
        content = "{4} {2}: {0}{3}{1}".format(red2, end, self.name, self.content, self.sign)
        return header + "\n" + content

    def __pos__(self):
        return None

    @classmethod
    def create(cls, value, name=''):
        return cls(value, name)


class Flag(Substance):
    def __init__(self, value, name=''):
        Substance.__init__(self, value, name)

    def __pos__(self):
        return 2 if self.content is None else int(self.content)


class Number(Substance):
    def __init__(self, value, name=''):
        Substance.__init__(self, value, name)

    def __pos__(self):
        if self.type != "complex":
            return '+' * (self.content > 0) + '0' * (self.content == 0) + '-' * (self.content < 0)


class DataStructure(Substance):
    def __init__(self, value, name=''):
        Substance.__init__(self, value, name)


class TimeData(Substance):
    def __init__(self, value, name=''):
        Substance.__init__(self, value, name)

    def __abs__(self):
        return Substance.__abs__(self).split('.')[1]


class Path(Substance):
    def __init__(self, value, name=''):
        Substance.__init__(self, value, path.split(value)[1] if not name else name)
        self.exist = path.exists(self.content)
        self.sign = sample.objects.get(self.type) if self.type != "ambiguous" else self.sign
        # self.sign = sample.files_properties.get(self.property)[1] if not self.property is None else self.sign
        self.dir = path.split(value)[0]

    def __abs__(self):
        if path.isdir(self.content):
            return "folder"
        elif path.isfile(self.content) or str(self.name).count('.') > 0 and str(self.name)[0] != '.':
            return "file"
        else:
            return "ambiguous"

    def __str__(self):
        header, content = Substance.__str__(self).split("\n")
        header += ", Exist: {0}{2}{1}, Dir: {0}{3}{1}".format(red2, end, self.exist, self.dir)
        return header + "\n" + content

    def __pos__(self):
        def get_key(value, dictionary):
            for key, value_list in dictionary.items():
                value_list = value_list if isinstance(value_list, list) else list(value_list)
                if value in value_list:
                    return key
            else:
                return None

        if self.type == "file":
            extension = self.name.split('.')
            return "Without extension" if len(extension) == 1 else get_key('.' + extension[1], sample.files)
        elif self.type == "folder":
            # TODO: def dir
            # return get_key(self.content, sample.dirs)
            return self.name
        else:
            return None


class String(Substance):
    def __init__(self, value, name=''):
        Substance.__init__(self, value, name)

    def __abs__(self):
        if len(self.content) == 1:
            return "char"
        elif str(self.content).count("\n") > 0:
            return "text"
        else:
            return "line"


def init(unknown_substance, name=''):
    for kind, match_condition in kinds_dict.items():
        if match_condition(unknown_substance):
            return kind(unknown_substance, name)


if __name__ == "__main__":
    def test_cases(mode):
        for i, (right_answer, test_case) in enumerate(sample.types.items()):
            user_answer = init(test_case)
            if mode == 0:
                print(str(user_answer))
            else:
                user = user_answer.kind + "_" + user_answer.type
                user += "_" + str(user_answer.exist) if user_answer.kind == "path" else ""
                print("{}: {}".format(i, red2 + str(test_case) + end))
                print("Expected answer: %s" % red2 + str(right_answer) + end)
                print("User answer: {}".format(red2 * (user == right_answer) + user + end))
            print()

    test_cases(0)
    test_value = "Hello! I'm Iri :)"
    item1 = init(test_value)
    print(str(item1))
    item2 = init([test_value])
    print(str(item2))
    item3 = init(None)
    print(item3)
