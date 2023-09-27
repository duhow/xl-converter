from HelperFunctions import stripPathToFilename
from statistics import mean

class Data():
    def __init__(self):
        self.items = []
        self.item_count = 0
        self.completed_items = []

        self.completion_times = []

    def __str__(self):
        output = ""
        for i in range(0,self.item_count):
            output += str(self.items[i][0]) + " | "
            output += str(self.items[i][1]) + " | "
            output += str(self.items[i][2]) + "\n"
        return output

    def parseData(self, root, allowed):  # root type is QTreeWidget.invisibleRootItem()
        """Populates the structure with proper data."""
        for i in range(root.childCount()):
            item = root.child(i)
            file_data = stripPathToFilename(item.text(2))
            if file_data[1].lower() in allowed:
                self.items.append(file_data)
            else:
                print(f"[Data] File not allowed for current format ({file_data[3]})")
        self.item_count = len(self.items)

    def getItem(self, n):
        return self.items[n]

    def getItemCount(self):
        return self.item_count
    
    def getCompletedItemsCount(self):
        return len(self.completed_items)
    
    def getTimeRemaining(self):
        completed_items_len = len(self.completed_items)
        if completed_items_len <= 2:
            return ""

        trailing_item_count = 15
        trailing_times = []

        if completed_items_len > trailing_item_count:
            for i in range(completed_items_len - trailing_item_count, completed_items_len):
                trailing_times.append(self.completion_times[i] - self.completion_times[i - 1])
        else:
            for i in range(1, completed_items_len):
                trailing_times.append(self.completion_times[i] - self.completion_times[i - 1])
            
        # Extrapolate
        time_remaining = round((self.getItemCount() - self.getCompletedItemsCount()) * mean(trailing_times))   # round to filter out noise
        h = int(time_remaining / 3600)
        m = int((time_remaining  / 60) % 60)
        s = int(time_remaining % 60)

        output = ""
        if h:   output += f"{h} h "
        if m:   output += f"{m} m "
        if s:   output += f"{s} s"

        return output
        
    def appendCompletionTime(self, n: float):
        self.completion_times.append(n)

    def appendCompletedItem(self, n):
        self.completed_items.append(n)
    
    def clear(self):
        self.items = []
        self.completed_items = []
        self.item_count = 0