## Requirement Engineering
All the feature requirements are avaliable in the [requirements.md](documentation/requirements.md) file, the file contains all the Functional and Non-Functional requirements along with corresponding User Stories.  

## Glossary
You can check the meaning of all technical terms used [here](documentation/glossary.md), and feel free to suggest any additions to our glossary or the documentation in general through the [issues](https://github.com/SeifAbdElrhman/T-Motor-Controller/issues) tab by opening a new issue with proper description and tag.  

## Design 
* The following **UML diagram** descibes our **Class structure** with main focus on dependencies.  

![Send](/documentation/Class_Diagram.png)

* The **Sequence Diagram** describes the usual sequence of operations of our system.  

![Send](/documentation/Sequence_Diagram.png)

* For **Design Patterns** we chose MVC (Model View Controller) as follows.

![Send](/documentation/Model_View_Controller.png)

We chose the MVC pattern because its the best pattern for our project, we needed our model to be seperate from our frontend to be able to optimize it without worring about compatibility with the frontend. this resuled in a couple of intermediate classes that facilitate communication between our model and our view (the frontend). These descision also had an unintended benfit of allowing people to design thier own frontend on top of our existing model. While maintaining our optimized communcation layer between the machine and the physical motor.

## Archtecture
* This is our static view diagram.  

![Send](/documentation/Static_View.png)

* And this is the Dynamic View of our system.

![Send](/documentation/Dynamic_View.png)
