package main


import (
    "fmt"
    "net/http"
    "io/ioutil"
)
 
func main() {
    response,_ := http.Get("http://192.168.217.11:8258/theme/getsets?pid=heyinliang&tid=vote&actid=1&orderby=hot&desc=1&start=0&count=10")
    defer response.Body.Close()
    body,_ := ioutil.ReadAll(response.Body)
    fmt.Println(string(body))
}
