/*
* Radix Tree in Go. <Copyright 2016 Lime lime.syh@gmail.com>
*
* `Get` run 10000000 times, about 2.7 seconds
*/

package main

import (
    "fmt"
    "net/http"
    "time"
)

const (
    ASTERISK = byte('*');
    COLON = byte(':');
    SLASH = byte('/');
)

func find(src string, target byte, start int, n int) (i int) {
    i = start
    for ; i < n && src[i] != target; i++ {}
    return
}

type Param struct {
    Key string
    Value string
}

type HandleFunc func(http.ResponseWriter, *http.Request, []Param)

type radixTreeNode struct {
    path string
    methods map[string]HandleFunc
    indices string
    children []*radixTreeNode
    maxParams int
}

func newRadixTreeNode(path string) (node *radixTreeNode) {
    node = &radixTreeNode{path: path}
    node.methods = make(map[string]HandleFunc)
    node.children = make([]*radixTreeNode, 0)
    return
}

func (node *radixTreeNode) addMethods(methods []string, handler HandleFunc) {
    for _, m := range methods {
        if _, ok := node.methods[m]; ok {
            panic("handler existed!")
        }
        node.methods[m] = handler
    }
}

func (node *radixTreeNode) getIndexPosition(target byte) int {
    low, high := 0, len(node.indices)
    for low < high {
        mid := low + ((high - low) >> 1)
        if node.indices[mid] < target {
            low = mid + 1
        } else {
            high = mid
        }
    }
    return low
}

func (node *radixTreeNode) insertChild(
        index byte, child *radixTreeNode) *radixTreeNode {

    i := node.getIndexPosition(index)

    node.indices = node.indices[:i] + string(index) + node.indices[i:]
    node.children = append(
        node.children[:i],
        append([]*radixTreeNode{child}, node.children[i:]...)...)

    return child
}

func (node *radixTreeNode) getChild(index byte) *radixTreeNode {
    i := node.getIndexPosition(index)
    if i == len(node.indices) || node.indices[i] != index {
        return nil
    }
    return node.children[i]
}

type RadixTree struct {
    root *radixTreeNode
}

func NewRadixTree() *RadixTree {
    return &RadixTree{newRadixTreeNode("")}
}

func (tree *RadixTree) Insert(
        path string, handler HandleFunc, methods []string) {

    i, n, root, maxParams := 0, len(path), tree.root, 0

    for i < n {
        if root.indices != "" && (root.indices[0] == ASTERISK ||
            path[i] == ASTERISK && root.indices != "" ||
            path[i] != COLON && root.indices[0] == COLON ||
            path[i] == COLON && root.indices[0] != COLON ||
            path[i] == COLON && root.indices[0] == COLON &&
            path[i + 1:find(path, SLASH, i, n)] != root.children[0].path) {

            panic("path conflict")
        }

        pos := root.getIndexPosition(path[i])
        if pos == len(root.indices) || root.indices[pos] != path[i] {
            pos = find(path, COLON, i, n)
            if pos == n {
                pos = find(path, ASTERISK, i, n)
                root = root.insertChild(path[i], newRadixTreeNode(path[i:pos]))

                if pos < n {
                    root = root.insertChild(
                        ASTERISK, newRadixTreeNode(path[pos + 1:]))
                    maxParams++;
                }

                root.addMethods(methods, handler)
                break
            }

            root = root.insertChild(path[i], newRadixTreeNode(path[i:pos]))
            i = find(path, SLASH, pos, n)
            root = root.insertChild(COLON, newRadixTreeNode(path[pos + 1:i]))
            maxParams++;

            if i == n {
                root.addMethods(methods, handler)
            }

        } else if path[i] == COLON {
            root = root.children[0]
            i += len(root.path) + 1
            maxParams++;

            if i == n {
                root.addMethods(methods, handler)
            }

        } else {
            root = root.getChild(path[i])

            j, m := 0, len(root.path)
            for j < m && i < n && path[i] == root.path[j] {
                i++;
                j++;
            }

            if j < m {
                child := newRadixTreeNode(root.path[j:])
                child.methods = root.methods
                child.indices = root.indices
                child.children = root.children

                root.path = root.path[:j]
                root.methods = make(map[string]HandleFunc)
                root.indices = string(child.path[0])
                root.children = []*radixTreeNode{child}
            }

            if i == n {
                root.addMethods(methods, handler)
            }
        }
    }

    if tree.root.maxParams < maxParams {
        tree.root.maxParams = maxParams
    }
}


func (tree *RadixTree) Get(path, method string) (
        found bool, handler HandleFunc, params []Param) {

    i, n, root, params := 0, len(path), tree.root, make(
        []Param, 0, tree.root.maxParams)

    for i < n {
        if len(root.indices) == 0 {
            return
        }

        if root.indices[0] == COLON {
            root = root.children[0]
            pos := find(path, SLASH, i, len(path))
            params = append(params, Param{root.path, path[i:pos]})
            i = pos

        } else if root.indices[0] == ASTERISK {
            root = root.children[0]
            params = append(params, Param{root.path, path[i:]})
            break
        } else {
            pos := root.getIndexPosition(path[i])
            if pos == len(root.indices) || root.indices[pos] != path[i] {
                return
            }

            root = root.children[pos]
            pos = i + len(root.path)

            if pos >= n || path[i:pos] != root.path {
                return
            }
            i = pos
        }
    }
    return true, root.methods[method], params
}


func User(w http.ResponseWriter, r *http.Request, params []Param) {
    fmt.Println(params)
}

func main() {
    tree := NewRadixTree()
    tree.Insert("/user", User, []string{"GET"})
    tree.Insert("/user/:name", User, []string{"GET"})
    tree.Insert("/user/:name/:sex/:age", User, []string{"GET"})
    tree.Insert("/src/*filename", User, []string{"GET"})

    fmt.Println(tree.Get("/user/Lime/male/25", "GET"))

    start := time.Now()
    for i := 0; i < 10000000; i++ {
        tree.Get("/user/Lime/male/25", "GET")
    }
    end := time.Now()
    fmt.Println(end.Sub(start))
}
