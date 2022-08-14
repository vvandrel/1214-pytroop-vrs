class Result:

    def __init__(self, result_code=0, result_description='Nothing has been executed!'):
        self.result_code = result_code
        self.result_description = result_description

    def __str__(self):
        return '[code: ' + str(self.result_code) + ', ' \
                'description: ' + self.result_description + ']'

    def set_result(self, result_code, result_description):
        self.result_code = result_code
        self.result_description = result_description
