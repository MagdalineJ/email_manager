    Email Manager is a Python-based project providing essential simulation of email functionalities 
    within a single GUI by TKinter library. Emails are introduced as messages throughout the design 
    and layout and the project doesn't imply the use or log-in of any real email. 
    The GUI opens with 700x500 pixels dimension containing a sidebar with four main buttons to
    navigate through pages. The main features of the buttons are listed below:
    =>ListMessages:Defaultpagedisplayingastructuredviewofallreceived messages.
    => ReadMessages:Upon entering a message ID in the input field,this button allows users to open 
    and view message content, with an option of changing priority for the selected message.
    => NewMessage:Thisbuttonleadstoasimplepagetocomposeandsendnew messages.
    => LabelMessages:Enablesuserstocategorisemessageswithcustomlabels provided by a dropdown list 
    for a categorized selection.


    Design and Development:
    Before designing the page layout, the functionalities of Email Manager have been studied.Email
    Manager created a separate window through the class of ReadMessage, where the class 
    ReadMessagesPage switches the page with similar layout through Tkinter frame in the enhanced
    simulation. The idea was to form integration of different pages to represent as a single GUI.
    The EmailManagerAPP Class that views a single GUI with multiple pages. Later, other classes 
    have been modified in methods to inherit child class from tk.Frame and to have a hierarchical 
    relationship with the main controller i.e. EmailManagerApp class.
    The sidebar remains almost the same while visiting different other pages, though there are two
    signifying innovations, that can be noticed. The current active page would have a blue 
    indicator on the side of the button and the footer in sidebar would be changed informing which
    button had been clicked.

    Another major difference is the enhanced version uses pack( ) instead of grid( ) for geometry
    management, resulting a responsive GUI creation. That leads the GUI to appear as more eye
    appealing, when the user makes the window larger. The messages are saved through a file with 
    Comma Separated Values Format (CSV). Later on in the file named “message_manager.py” new 
    functions have been created and modified to initialise, load and save messages to “messages.CSV”. 
    The structure how the messages are to be saved are reused with the given file “message.py”.

    ReadMessagesPage frame is cleared every time any button is clicked, and any message is 
    displayed.The default page displays List Messages, with a structure of messages with their 
    ID no, priority displayed as stars, sender’s email address, designated label and subject. 
    However, innovation has been made with adding a filter option which helps to search any keyword
    that is contained by any sections of the message i.e. sender, recipient, subject and message 
    content. The Search button is disabled in the default page. It only enables when a text or number
    or character has been inserted. When the Search button is clicked it displays the messagebox 
    confirming the location where it has found the keyword and displays the message, so that user
    can easily navigate to locate the message. On the other hand, if the section doesn’t contain the
    keyword, it is updated by another messagebox and the message list remains unchanged. Refresh 
    button helps viewing all the saved messages.

    Title label of the NewMessagePage class “Compose a New Message”, which is interacted through 
    New Message button, provides an idea of the functionality of New Message page. The design 
    layout is like Read Message page, with fields for sender, recipient, subject, message content
    and priority. The buttons i.e., Send and Close however are different with functionalities. Send
    button helps sending the message and saving it in the CSV file. After sending and clicking the 
    Close button, the default message page is triggered to view all messages, which is updated by the
    new message as well.
    Another frame of Email Manager GUI is Label Messages, which lets user to search the messages 
    according to the dropdown list, when the List Messages button is clicked. To add a new label 
    user needs to select label and input message ID, then click the button Add Label (figure-7). The Back button helps viewing List Messages page.

    However, if the label doesn’t exist, the message box appears to update, and the GUI appearance 
    changes.

    Unlike List Messages page where Tkinter Combobox has been used for drop down list, Label Message
    page uses Tkinter OptionMenu to view the labels. These diNerences have enabled the appearance of 
    design for both drop down list unique.

    Error Handling:
    1) ReadMessagesPage:The ID field and priority field has been modified to reject invalid number
    figures. These display error message identifying the cause of rejection to use the corresponding
    functionality.
    2) ListMessagesPage:The Filter by optionis controlled by two functionalities: the dropdown list
    of sections that limits the scope of searching and the input value handling, which is done by
    disabling Search button when the input field is empty or only spaces has been put as keywords.
    3) NewMessagePage:The fields of NewMessagePage are valid ted to reject empty values in order to
    send the message. The email address fields also useregular expression (re), which then compares 
    the input with “email_regex” variable to validate email.
    4) LabelMessagesPage:While adding the label possibl eerror of string input and invalid ID input
    has been handled by message box appearance. The “list _txt” field has been disabled for any user
    input, to prevent unauthorised changes and protect information.


    Testing and Faults:
    To test the functionalities Unit test has been completed with each of the classes of Email 
    Manager GUI, through PyTest. The tests check whether the UI functions properly, i.e., page 
    navigation, button interactions, error handling and sidebar interactions are smoothly handled.
    There has been a test for each method or major functions of classes. While writing the test 
    functions, assertIN( ) and assertequal( ), mock( ), patch( ) and fixture have been used from 
    unittest library ()  .
    Although all the functionalities are working fine and most of the test results has passed, test
    of NewMessagePage class for sending a message with valid input has failed. The error encountered 
    is, to send a message successfully new_message( ) function from message_manager needs to be 
    called in NewMessagePage , but while testing the following function was called 0 times.