class IVR:

  def __init__(self, intro, iterable, items, **kwargs):
      '''
      Creates the IVR object by generating the initial prompt

        Parameters:
          intro (string): The introduction sentence to the IVR
          iterable (string): A template string to be filled in by the items
          items (dict): A dictionary of items with a name and phone number
      '''
      self.intro = intro
      self.iterable = iterable
      self.items = items
      self.phone_number_table = {}
      self.valid_inputs = ''
      self.prompt = self.intro
      length = len(self.items)
      ## iterate over the items list and build the selection menu
      ## Sets the phone_number_table to lookup phone number from digit
      for i in range(length):
          itemName = self.items[i]['itemName']
          phone_number = self.items[i]['phoneNumber']
          digit = str(i+1) #cast to string and +1 (0-index)
          prompt = self.iterable % (itemName, digit)
          self.prompt = f'{self.prompt}, {prompt}'
          self.phone_number_table[digit] = phone_number
          self.valid_inputs = f'{self.valid_inputs}{digit}'

  def get_prompt(self):
      return self.prompt

  def get_valid_digits(self):
      return self.valid_inputs

  def get_phone_number_from_digit(self, digit):
      if (digit in self.phone_number_table):
          return self.phone_number_table[digit]
      else:
          return False
