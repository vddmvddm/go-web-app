package main

import "fmt"

type Person struct {
	name          string
age           int
}

func (p *Person) GetName() string {
    return p.name
}

func (p *Person) SetName(newName string) {
    p.name = newName
}

// Unused function
func (p *Person) setNamePrivate(newName string) {
	p.name = newName
}

func main() {
    person := Person{"John", 30}
    person.SetName("John Doe")
    fmt.Println(person.GetName())

    if person.age >= 18 {
		fmt.Println("Adult")
	} else {
        fmt.Println("Minor")
    }

    var personsAge = 25
    if personsAge >= 18 {
	fmt.Println("Adult")
	} else {
    fmt.Println("Minor")
}

	var unusedVar string // Unused variable
}
