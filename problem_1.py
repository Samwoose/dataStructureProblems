class DoubleNode:
    def __init__(self, value, key):
        self.key = key
        self.value = value
        self.next = None
        self.previous = None
        
class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
    
    def append(self, value, key):
        
        # TODO: Implement this method to append to the tail of the list
        if self.head is None:
            self.head = DoubleNode(value, key)
            self.tail = self.head
        elif self.tail is self.head and self.tail is not None:
            self.tail = DoubleNode(value, key)
            self.tail.previous = self.head
            self.head.next = self.tail
        else:
            temp_node = self.tail
            self.tail = DoubleNode(value, key)
            self.tail.previous = temp_node 
            temp_node.next = self.tail
            
    def addHead(self,value, key):
        if self.head is None:
            self.head = DoubleNode(value, key)
            self.tail = self.head
        elif self.tail is self.head and self.tail is not None:
            new_head = DoubleNode(value, key)
            new_head.next = self.head
            self.head = new_head
            self.tail.previous = self.head
        else:
            new_head = DoubleNode(value, key)
            new_head.next = self.head
            self.head.previous = new_head
            self.head = new_head
            
    def removeTail(self):
        if self.tail is self.head and self.tail is not None:
            self.head = None
            self.tail = None
        elif self.head is None:
            return
        else:
            new_tail = self.tail.previous
            new_tail.next = None
            self.tail.previous = None
            self.tail = new_tail
            
    def removeMiddle(self,middleNode):
        previousNode = middleNode.previous
        nextNode = middleNode.next
        
        #reconnecting
        previousNode.next = nextNode
        nextNode.previous = previousNode
        
        #remove connection in middle node
        middleNode.next = None
        middleNode.previous = None
        
    def removeHead(self):
        if self.tail is self.head and self.tail is not None:
            self.head = None
            self.tail = None
        elif self.head is None:
            return
        else:
            new_head = self.head.next
            new_head.previous = None
            self.head.next = None
            self.head = new_head
            
    def to_list(self):
        out_list = []

        node = self.head
        while node:
            out_list.append([node.key,node.value])
            node = node.next

        return out_list
            
            
class LRU_Cache(object):

    def __init__(self, capacity):
        # Initialize class variables
        self.capacity = capacity
        self.doublell = DoublyLinkedList()
        self.keyLocDict = {}

    def get(self, key):
        # Retrieve item from provided key. Return -1 if nonexistent. 
        if key in self.keyLocDict:
            temp_node = self.keyLocDict[key]
            temp_value = temp_node.value
            
            #remove the existing node and add it as most recently used cache 
            self.removeHelper(temp_node)
            self.doublell.addHead(temp_value,key)
            
            #update new node location
            self.keyLocDict[key] = self.doublell.head
            
            return self.keyLocDict[key].value
        else:
            return -1
    def removeHelper(self,targetNode):
        if targetNode is self.doublell.head and targetNode is self.doublell.tail:
            self.doublell.removeTail()
        elif targetNode is self.doublell.head and targetNode is not self.doublell.tail:
            self.doublell.removeHead()
        elif targetNode is not self.doublell.head and targetNode is self.doublell.tail:
            self.doublell.removeTail()
        else:
            self.doublell.removeMiddle(targetNode)
        
    
    def set(self, key, value):
        # Set the value if the key is not present in the cache. If the cache is at capacity remove the oldest item. 
        if key not in self.keyLocDict:
            if len(self.keyLocDict) < self.capacity:
                #print('here1')
                self.doublell.addHead(value,key)
                self.keyLocDict[key] = self.doublell.head
                #print(self.doublell.to_list())
                #print(self.keyLocDict)
            else:
                #print('here2')
                LRUKey = self.doublell.tail.key
                
                #remove the least recently used key and its value from doubly ll and hash map
                self.doublell.removeTail()
                del self.keyLocDict[LRUKey]
                
                #add new key and value
                self.doublell.addHead(value,key)
                self.keyLocDict[key] = self.doublell.head
        else:
            return    