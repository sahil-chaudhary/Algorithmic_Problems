import abc
import matplotlib.pyplot as plt

# this class characterizes an automaton
class FSA:
    def __init__ (self, numStates = 0, startStates=None, finalStates=None, alphabetTransitions=None) :
        self.numStates = numStates
        self.startStates = startStates
        self.finalStates = finalStates
        self.alphabetTransitions = alphabetTransitions


class NFA(FSA):
    def simulate(self, ipStr):
        S = set(self.startStates)
        newS = set()
        for i in range(len(ipStr)):
            symbol = ipStr[i]
            tm = self.alphabetTransitions[symbol]
            for state in S:
                trs = tm[state]
                for tr in range(len(trs)):
                    if trs[tr] == 1:
                        newS.add(tr)
            S = set(newS)
            newS = set()
        if len(self.finalStates) > 0 and not S.isdisjoint(self.finalStates):
            print("String Accepted")
            return True
        else:
            print("String Rejected")
            return False

    def getNFA(self):
        return self

class ETree:
    root = None
    nfa = None
    class ETNode:
        def __init__(self, val=" ", left=None, right=None):
            self.val = val
            self.left = left
            self.right = right

    

    def compute(self, operands, operators):
            operator = operators.pop()
            if operator == "*":
                left = operands.pop()
                operands.append(self.ETNode(val=operator, left=left))
            elif operator == "+":
                right, left = operands.pop(), operands.pop()
                operands.append(self.ETNode(val=operator, left=left, right=right))
            elif operator == ".":
                right, left = operands.pop(), operands.pop()
                operands.append(self.ETNode(val=operator, left=left, right=right))

    def parseRegex(self, regex):
        operands, operators = [], []
        for i in range(len(regex)):
            if regex[i].isalpha():
                operands.append(self.ETNode(val=regex[i]))
            elif regex[i] == '(':
                operators.append(regex[i])
            elif regex[i] == ')':
                while operators[-1] != '(':
                    self.compute(operands, operators)
                operators.pop()
            else :
                operators.append(regex[i])
        while operators:
            self.compute(operands, operators)

        if len(operators) == 0:
            self.root = operands[-1]
        else :
            print("Parsing Regex failed.")

    def getTree(self):
        return self.root

    ###################################################################
    # IMPLEMENTATION STARTS AFTER THE COMMENT
    # Implement the following functions

    # In the below functions to be implemented delete the pass statement
    # and implement the functions. You may define more functions according
    # to your need.
    ###################################################################
    # .
   
    def operatorDot(self, fsaX, fsaY):
        """OperatorDot function takes two FSAs as input and returns a new FSA that is the concatenation of the two input FSAs.
        Args:
            fsaX: FSA object
            fsaY: FSA object
            Returns:
            FSA: FSA object
        Implementation:
        1. Create a new FSA with the number of states equal to the sum of the number of states in the two input FSAs.
        2. Add the start states of the first input FSA to the start states of the new FSA. If epsilon is in the language of the first FSA, add the start states of the second FSA to the start states of the new FSA.
        3. Add the final states of the second input FSA to the final states of the new FSA. If epsilon is in the language of the second FSA, add the final states of the first FSA to the final states of the new FSA. The epsilon in the language of the second FSA is vacuously handled."""    
        
        #Handle case if input is invalid or not available
        if fsaX == None or fsaY == None:
            raise ValueError("FSA is not available")
        
        #Extract Information from the input FSA and create new states
        num_states = fsaX.numStates + fsaY.numStates
        start_states = set()
        for state in fsaX.startStates:
            start_states.add(state)

        
        #Extract states in Y for FSA and add the number of states in X to each state in Y
        final_states = set()
        for state in fsaY.finalStates:
            state=state+fsaX.numStates
            final_states.add(state)
            
        symbols = set(fsaX.alphabetTransitions.keys()).union(set(fsaY.alphabetTransitions.keys())) #Get the union of the alphabets of the two FSAs
        alphabet_transitions = {}

       
        #Copy the data from the input FSA to the new FSA 
        for symbol in symbols:
            transitions = [[0 for i in range(num_states)] for j in range(num_states)]
            for i in range(num_states):
                for j in range(num_states):
                    if symbol in fsaX.alphabetTransitions:
                        if i<fsaX.numStates and j<fsaX.numStates:
                            transitions[i][j] = fsaX.alphabetTransitions[symbol][i][j]
                    if symbol in fsaY.alphabetTransitions:
                        if i>=fsaX.numStates and j>=fsaX.numStates:
                            transitions[i][j] = fsaY.alphabetTransitions[symbol][i-fsaX.numStates][j-fsaX.numStates]
            alphabet_transitions[symbol] = transitions
        
        #Add transitions from prefinal states of X to start states of Y
        for symbol in fsaX.alphabetTransitions:
            for i in range(fsaX.numStates):
                for state in fsaX.finalStates:
                    if symbol in fsaX.alphabetTransitions:
                        if alphabet_transitions[symbol][i][state]==1:
                            for j in fsaY.startStates:
                                alphabet_transitions[symbol][i][j+fsaX.numStates] = 1 #Add transition from prefinal of X to start state of Y with the same symbol 
        
        #Handle the case if epsilon in the language of fsaX. epsilon in fsaY is vacously handled from previous case. But, what if epsilon is in fsaX?
        for start in fsaX.startStates:
            for final in fsaX.finalStates:
                if start == final :
                    # need to add start state of Y also to be the start state of the new FSA
                    for state in fsaY.startStates:
                        start_states.add(state+fsaX.numStates)

        
        #Handle the case if epsilon is in the regex. No need to add epsilon transitions anywhere. Just make sure that capture the idea of delta for epsilon. i.e.
        # we go from state i to state i if we see epsilon. This way, if e is in the string, we can just stay at the same state and the NFA will accept the string
        #Idea is to create a identity matrix and store the transitions for epsilon in the alphabet_transitions
        transitions = [[0 for i in range(num_states)] for j in range(num_states)]
        for i in range(num_states):
            for j in range(num_states):
                if i==j:
                    transitions[i][j] = 1
        alphabet_transitions['e'] = transitions

        return FSA(numStates=num_states, startStates=start_states, finalStates=final_states, alphabetTransitions=alphabet_transitions)
    # +
    def operatorPlus(self, fsaX, fsaY):
        """OperatorPlus function takes two FSAs as input and returns a new FSA that is the union of the two input FSAs.
        Args:
            fsaX: FSA object
            fsaY: FSA object
            Returns:
            FSA: FSA object
            Implementation:
            1. Create a new FSA with the number of states equal to the sum of the number of states in the two input FSAs.
            2. Add the start states of the fsaX and fsaY to the start states of the new FSA.
            3. Add the final states of the fsaX and fsaY to the final states of the new FSA.
            4. Copy the transitions from the input FSAs to the new FSA.
            Since multiple start states are allowed, we can just add the start states of the two input FSAs to the start states of the new FSA. Similarly, we can add the final states of the two input FSAs to the final states of the new FSA. The transitions from the input FSAs can be directly copied to the new FSA."""
        #Handle case if input is invalid or not available
        if fsaX == None or fsaY == None:
            raise ValueError("FSA is not available")

        #Extract Information from the input FSA and create new states
        num_states = fsaX.numStates + fsaY.numStates  #Add one more states and create epsilon transitions from new start state to start states of X and Y
        start_states = set()
        for state in fsaX.startStates:
            start_states.add(state)
        for state in fsaY.startStates:
            start_states.add(state+fsaX.numStates)
        
        final_states = set()
        for state in fsaX.finalStates:
            final_states.add(state)
        for state in fsaY.finalStates:
            final_states.add(state+fsaX.numStates)
        
        alphabet_transitions = {}
        symbols = set(fsaX.alphabetTransitions.keys()).union(set(fsaY.alphabetTransitions.keys()))

        #Copy the data from the input FSA to the new FSA and we are done since multiple start states are allowed.
        for symbol in symbols:
            transitions = [[0 for i in range(num_states)] for j in range(num_states)]
            for i in range(num_states):
                for j in range(num_states):
                    if symbol in fsaX.alphabetTransitions:
                        if i<fsaX.numStates and j<fsaX.numStates:
                            transitions[i][j] = fsaX.alphabetTransitions[symbol][i][j]
                    if symbol in fsaY.alphabetTransitions:
                        if i>=fsaX.numStates and j>=fsaX.numStates:
                            transitions[i][j] = fsaY.alphabetTransitions[symbol][i-fsaX.numStates][j-fsaX.numStates]
            alphabet_transitions[symbol] = transitions

        #Handle the case if epsilon is in the regex. No need to add epsilon transitions anywhere. Just make sure that capture the idea of delta for epsilon. i.e.
        # we go from state i to state i if we see epsilon. This way, if e is in the string, we can just stay at the same state and the NFA will accept the string
        #Idea is to create a identity matrix and store the transitions for epsilon in the alphabet_transitions
        transitions = [[0 for i in range(num_states)] for j in range(num_states)]
        for i in range(num_states):
            for j in range(num_states):
                if i==j:
                    transitions[i][j] = 1
        alphabet_transitions['e'] = transitions
        
       

        return FSA(numStates=num_states, startStates=start_states, finalStates=final_states, alphabetTransitions=alphabet_transitions)


    # *
    def operatorStar(self,fsaX):
        """OperatorStar function takes an FSA as input and returns a new FSA that is the Kleene star of the input FSA.
        Args:
            fsaX: FSA object
            Returns:
            FSA: FSA object
            Implementation:
            1. Create a new FSA with the number of states equal to the number of states in the input FSA plus 2.
            2. Add a new start state to the start states of the new FSA.
            3. Add a new final state to the final states of the new FSA.
            4. Copy the transitions from the input FSA to the new FSA.
            5. All the outgoing transitions from the start states of the input FSA should be copied to the start state of the new FSA. After achieving this, Similarly, all the incoming transitions to the final states of the input FSA should be copied to the final state of the new FSA.
            6. Now, collapse These new two states into one and we are done"""
        #Handle case if input is invalid or not available
        if fsaX is None:
            raise ValueError("FSA is not available")

        #Extract Information from the input FSA and create new states
        num_states = fsaX.numStates + 2 #Add two more state e and g a
        
        start_states = 0 #Introducing state 0 as both start and final state
        final_states = 0
        
        symbols = set(fsaX.alphabetTransitions.keys())
        alphabet_transitions = {}
        alphabet_transitions2 = {}
       

        #Copy the data from the input FSA to the new FSA
        for symbols in fsaX.alphabetTransitions:
            transitions = [[0 for i in range(num_states)] for j in range(num_states)]
            transitions2 = [[0 for i in range(num_states-1)] for j in range(num_states-1)]
            for i in range(num_states):
                for j in range(num_states):
                    if i>1 and j>1:
                        transitions[i][j] = fsaX.alphabetTransitions[symbols][i-2][j-2]
                    if (i>0 and j>0) and (i<num_states-1 and j<num_states-1):
                        transitions2[i][j] = fsaX.alphabetTransitions[symbols][i-1][j-1]
            alphabet_transitions2[symbols] = transitions2
            alphabet_transitions[symbols] = transitions
        
        #For every transition state from start state, copy the outgoing edges to e(0 in our case)and for every incoming edge to final state, copy the incoming edges to (1 in our case)
        for symbol in fsaX.alphabetTransitions:
            for i in range(num_states):
                for states in fsaX.startStates:
                    if alphabet_transitions[symbol][states+2][i]==1:
                        alphabet_transitions[symbol][0][i] = 1
        for symbol in fsaX.alphabetTransitions:
            for i in range(num_states):
                for states in fsaX.finalStates:
                    if alphabet_transitions[symbol][i][states+2]==1:
                        alphabet_transitions[symbol][i][1] = 1
        
        

        #Fuse 'e' and 'g' together. In this sense, we introduce new state h and all the transition relations from e to X and X to g are now from h to X and from X to h
        for symbol in fsaX.alphabetTransitions:
            for i in range(num_states):
                if alphabet_transitions[symbol][0][i]==1:
                    alphabet_transitions2[symbol][0][i-1]=1
                if alphabet_transitions[symbol][i][1]==1:
                    alphabet_transitions2[symbol][i-1][0]=1

        
        alphabet_transitions = alphabet_transitions2
        num_states = num_states-1

        #Handle the case if epsilon is in the regex. No need to add epsilon transitions anywhere. Just make sure that capture the idea of delta for epsilon. i.e.
        # we go from state i to state i if we see epsilon. This way, if e is in the string, we can just stay at the same state and the NFA will accept the string
        #Idea is to create a identity matrix and store the transitions for epsilon in the alphabet_transitions
        transitions = [[0 for i in range(num_states)] for j in range(num_states)]
        for i in range(num_states):
            for j in range(num_states):
                if i==j:
                    transitions[i][j] = 1
        alphabet_transitions['e'] = transitions
        

        return FSA(numStates=num_states, startStates={start_states}, finalStates={final_states}, alphabetTransitions=alphabet_transitions)
                    
       #Add epsilon transitions from final states to start state
        


    # a, b, c and e for epsilon
    def alphabet(self, symbol):
        """Alphabet function takes a symbol as input and returns a new FSA that accepts the symbol.
        Args:symbol: string
        Returns: FSA: FSA object"""
        #Handle epsilon case since it is a special case
        if symbol == 'e':  
            new_state = 0
            num_states = 1
            final_states = 0
            #Assuming that a,b,c are the only alphabets that are going to be used
            transitions = { 'a': [[0]], 'b': [[0]], 'c': [[0]]}
        else:
            #Handle the case for a single alphabet
            new_state = 0  
            num_states = 2
            final_states = 1
            transitions = { symbol: [[0,1],[0,0]]}
        return FSA(numStates=num_states, startStates={new_state}, finalStates={final_states}, alphabetTransitions=transitions)
    

    # Traverse the regular expression tree(ETree)
    # calling functions on each node and hence
    # building the automaton for the regular
    # expression at the root.
    
    def buildNFA(self, root):
        """buildNFA function takes a regular expression tree as input and returns a new FSA that accepts the language of the regular expression.
        Args:
            root: ETree object
            Returns:
            FSA: FSA object
            Implementation:
            1. Traverse the regular expression tree in a post-order fashion.
            2. For each node, call the appropriate function to build the FSA for the subexpression rooted at the node.
            3. Return the FSA for the entire regular expression."""
        if root == None:
            print("Tree not available")
            exit(0)

        numStates = 0
        initialState = set()
        finalStates = set()
        transitions = {}

        #I felt recursively calling left subtree and then right subtree is better than using a stack to traverse the tree
        nfa = self.buildnfarecursive(root)
        
        # Set the final NFA object attributes
        self.nfa = nfa
        
        return NFA(numStates=nfa.numStates, startStates=nfa.startStates, finalStates=nfa.finalStates, alphabetTransitions=nfa.alphabetTransitions)
    
    def buildnfarecursive(self, root):
        if root == None:
            return None
        if root.val.isalpha():
            return self.alphabet(root.val)
        elif root.val == ".":
            return self.operatorDot(self.buildnfarecursive(root.left), self.buildnfarecursive(root.right))
        elif root.val == "+":
            return self.operatorPlus(self.buildnfarecursive(root.left), self.buildnfarecursive(root.right))
        elif root.val == "*":
            return self.operatorStar(self.buildnfarecursive(root.left))
        else:
            print("Invalid regex")
            return None
        
    
    ######################################################################

