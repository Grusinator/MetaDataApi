from datetime import datetime


class DataTypeUtils:

    @staticmethod
    def identify_data_type(element):
        if element is None:
            return None

        def test_float(elm):
            assert ("." in elm), "does not contain decimal separator"
            return float(elm)

        def test_bool(elm):
            trues = ("true", "True")
            falses = ("false", "False")

            if elm in trues:
                return True
            elif elm in falses:
                return False
            else:
                raise ValueError("is not either true or false")

        def test_datetime(text):
            try:
                return dateutil.parser.parse(text)
            except:

                datetime_formats = (
                    '%Y-%m-%dT%H: %M: %SZ',  # strava
                )

                for fmt in datetime_formats:
                    try:
                        return datetime.strptime(text, fmt)
                    except ValueError as e:
                        pass

                raise ValueError('no valid date format found')

        # even though it is a string,
        # it might really be a int or float
        # so if string verify!!
        if isinstance(element, str):
            conv_functions = {
                float: test_float,
                int: lambda elm: int(elm),
                datetime: test_datetime,
                str: lambda elm: str(elm),
                bool: test_bool
            }

            order = [float, int, datetime, bool, str]

            for typ in order:
                try:
                    # try the converting function of that type
                    # if it doesnt fail, thats our type
                    return conv_functions[typ](element)
                except (ValueError, AssertionError) as e:
                    pass

            # if nothing else works, return as string
            return str(element)

        elif isinstance(element, (float, int, bool)):
            # otherwise just return the type of
            return element
