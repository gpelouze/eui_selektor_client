class FormFields:
    class _Base:
        def __init__(self, name, comment=None):
            self.name = name
            self.comment = comment

        @property
        def comment_repr(self):
            if self.comment is not None:
                return f'  # {self.comment}'
            else:
                return ''

    class Number(_Base):
        def __init__(self, name, min_val, max_val, comment=None):
            super().__init__(name, comment=comment)
            self.min = min_val
            self.max = max_val

        def __repr__(self):
            s = f'{self.name}: number ({self.min}-{self.max})'
            s += self.comment_repr
            return s

    class Date(_Base):
        def __init__(self, name, date, comment=None):
            super().__init__(name, comment=comment)
            self.date = date

        def __repr__(self):
            s = f"{self.name}: date ('YYYY-MM-DD')"
            s += self.comment_repr
            return s

    class _Choice(_Base):
        def __init__(self, name, options, comment=None):
            super().__init__(name, comment=comment)
            self.options = options

        @property
        def options_repr(self):
            options_repr = [repr(opt) for opt in self.options]
            return ', '.join(options_repr)

    class SingleChoice(_Choice):
        def __repr__(self):
            s = f'{self.name}: list (choices: {self.options_repr})'
            s += self.comment_repr
            return s

    class MultipleChoice(_Choice):
        def __repr__(self):
            s = f'{self.name}: string (choices: {self.options_repr})'
            s += self.comment_repr
            return s