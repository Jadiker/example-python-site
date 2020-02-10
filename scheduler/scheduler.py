import re
from functools import wraps

'''Conversions.py'''
'''This has a bunch of functions for converting from some time formats to other time formats'''

#An exception class for this class to use when it fails
class ConversionFailed(RuntimeError):
    pass

#s is a string
#repList is a dictionnary in the form {replacementSubstring1:[substringToBeReplaced1.1, substringToBeReplaced1.2, ...], replacementSubstring2:[substringToBeReplaced2.1, substringToBeReplaced2.2, ...], ...]
def multipleReplace(s, reps):
    for rep in reps:
        for toLookFor in reps[rep]:
            s = s.replace(toLookFor, rep)
    return s

#a decorator that makes the method static, and if the method would fail with an Exception, it raises ConversionFailed(failString) instead
def conversionmethod(func):
    @staticmethod
    @wraps(func)
    def conversionmethod_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        #upgrade: if the exception is a ConversionFailed, then just reraise it, otherwise raise this default one
        except Exception as e:
            raise ConversionFailed(func.__name__+" failed to convert {}.\nThe error is:\n{}".format(args, e))
    return conversionmethod_wrapper

class Conversions:
    #ExpandedQuickTime is like a QuickTime except for the 'h' and 'm' can be written out as words as well.
    @conversionmethod
    def extendedQuickTimeToMinutes(timeString):
        timeString = timeString.strip()
        equation = multipleReplace(timeString, {'+':['minutes', 'minute', 'min', 'm'], '*60+':['hours', 'hour', 'h']})
        if equation[-1]=='+':
            equation = equation[:-1]
        #TODO stop using eval
        try:
            return eval(equation)
        except Exception:
            raise ConversionFailed("Could not convert {} into a time".format(timeString))

    #mins is always a number, not a string
    #HourTuple is time in the form (1, 5), where the first value is the hours and the second value is the minutes
    @conversionmethod
    def minutesToHourTuple(mins):
        return (mins//60, mins%60)

    @conversionmethod
    def hourTupleToMinutes(h, m):
        return 60*h+m

    #StringHourTuple is time in the form ('1', '5'), where the first value is the hours and the second value is the minutes
    @conversionmethod
    def minutesToStringHourTuple(mins):
        h, m = Conversions.minutesToHourTuple(mins)
        return (str(h), str(m))

    #QuickTime is a time like '1h 5m'
    @conversionmethod
    def minutesToQuickTime(mins):
        hours, minutes = Conversions.minutesToStringHourTuple(mins)
        #upgrade: code duplication in minutesToCompleteTime
        if hours!="0":
            if minutes!="0":
                return hours+'h '+minutes+'m'
            else:
                return hours+'h'
        else:
            return minutes+'m'

    #Completetime is like "1 hour and 5 minutes"
    @conversionmethod
    def minutesToCompleteTime(mins, default = "no time at all"):
        times = list(Conversions.minutesToHourTuple(mins))
        words = ["hours", "minutes"]
        howMany = 2 #hours is one, minutes is one. Since both are active right now, we have 2.
        for index, time in enumerate(times):
            if time==1: #make the word not plural
                words[index] = words[index][:-1]
            if time==0: #delete the word because there is no time there
                words[index] = ""
                howMany-=1 #one of the words is no longer needed

        if howMany==2: #both hours and minutes
            return "{} {} and {} {}".format(times[0], words[0], times[1], words[1])
        elif howMany==1: #just one or the other
            for index, word in enumerate(words):
                if word:
                    return "{} {}".format(times[index], words[index])
        else:
            return default #if the time is 0 minutes, return the default string

    #colonedTime is like "3:00" or just "3"
    @conversionmethod
    def colonedTimeToMinutes(s):
        #convert it into a (extended) quicktime
        colonIndex = s.find(":")
        if colonIndex>0: #it does have a colon
            #replace the colon with 'h' and tack an 'm' onto the end
            s = s[:colonIndex]+'h'+s[colonIndex+1:]+'m'
        else: #no colon
            #tack an 'h' onto the end
            s+='h'
        return Conversions.extendedQuickTimeToMinutes(s)


class SchedulerError(RuntimeError):
    pass

class IncorrectFormError(SchedulerError):
    pass

class NoTimeError(SchedulerError):
    pass


#compatibility with Python 2
try:
    input = raw_input
except NameError:
    pass

#This is the main class of the program.
#It keeps track of the schedule and to-do list and makes them work together
class Scheduler:
    def __init__(self):
        self.todoList = []
        self.schedule = []

    def addTextTodo(self, txt):
        #regex search for open paren followed by smallest amount of letters (at least one though) until close paren followed by space until end
        #the goal is to get whatever's in the last set of parentheses
        #the list comprehension is so that we can find the last set of parentheses (I couldn't find any other way to do it)
        pTimes = [[match.start(), match.group(1)] for match in re.finditer(r'\((.+?)\)\s*', txt)] #short for 'potentialTimes'
        try:
            pTimes = pTimes[-1] #only care about the last set of parentheses #this is what will throw the error if nothing is found
            timeString = pTimes[1].strip() #take out the whitespace and get just the captured stuff inside the parenthesis
            time = Conversions.extendedQuickTimeToMinutes(timeString) #this will throw an error if the time isn't right
        except (IndexError, ConversionFailed):
            raise NoTimeError("No time found in the task '{}'".format(txt))
        name = txt[:pTimes[0]].strip()
        self.todoList.append(Todo(name, time))

    #upgrade: AM and PM settings
    def addTodoToSchedule(self, plannedTodo):
        def getInfo(pT): #pT is short for plannedTodo
            #TODO what happens if someone does '\d:\d' as a time, without the second digit? Could use lookahead.
            m = re.match(r'\s*(\d\d?:?\d?\d?)\s*-\s*(\d\d?:?\d?\d?)\s*\(\s*(\d+)\)\s*', plannedTodo)
            if m:
                sCT, eCT, todoHNS = m.groups() #short for startColonedTime, endColonedTime, and todoHumanNumberString
                start = Conversions.colonedTimeToMinutes(sCT)
                end = Conversions.colonedTimeToMinutes(eCT)
                num= int(todoHNS)-1 #convert it back to the number the computer uses (starting at 0 instead of 1)
                return start, end, num
            else:
                raise(IncorrectFormError("Could not add '{}' to the schedule because it was in the incorrect form.".format(plannedTodo)))

        #start and end are both times in minutes, todoNum is the number of the to-do
        start, end, todoNum = getInfo(plannedTodo)
        theTodo = self.todoList[todoNum]
        theTodo.timeLeft-=end-start
        self.schedule.append([start, end, theTodo])
        return theTodo

#todos have a
#name, time to complete the task, a potential due date, and how much time is left to complete the task
class Todo:
    def __init__(self, name, totalTime = None, dueDate = None):
        self.name = name
        self.totalTime = totalTime
        self.dueDate = dueDate
        self.timeLeft = self.totalTime

    def __str__(self):
        #return "Todo object: [name = '{}', time = '{}']".format(self.name, self.time)
        return "{} ({} minutes)".format(self.name, self.totalTime)

def main(user_input):
    '''Takes in input with newlines separating each task and returns the string totalling the time'''
    ans = ""
    try:
        schedule = Scheduler()
        user_input_lines = user_input.split("\n")
        while user_input_lines:
            inputText = user_input_lines.pop(0)
            try:
                schedule.addTextTodo(inputText)
            except NoTimeError:
                pass

        ans += "Here is your to-do list:\n"
        timeSum = 0 #this will also sum the time as we go through the list
        for index, todo in enumerate(schedule.todoList):
            #using human indexes
            ans += "({}) {} ({})\n".format(index+1, todo.name, Conversions.minutesToQuickTime(todo.totalTime))
            timeSum+=todo.totalTime
        ans += "\nToday's to-dos will take {} to complete.".format(Conversions.minutesToCompleteTime(timeSum))
        return ans
    except Exception:
        return traceback.format_exc()
