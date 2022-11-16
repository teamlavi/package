/*
Copyright © 2022 NAME HERE <EMAIL ADDRESS>

*/
package main

import (
	"fmt"
	"lavi/cmd"
	"log"
)

func main() {
	defer func() {
		// this allows for a clean exit on unexpected errors
		if err := recover(); err != nil {
			fmt.Println("unhandled exception occured")
			if e, ok := err.(error); ok {
				fmt.Println(e.Error())
			}
		}
	}()
	log.SetFlags(0)
	cmd.Execute()
}
