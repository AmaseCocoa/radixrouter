/*
* Radix Tree in C++
*/

#include "tree.h"

namespace radixtree {

Request::Request(string path, string method) {
  this->path = path;
  this->method = method;
}

RadixTreeNode::RadixTreeNode(string path) {
  this->path = path;
}

int RadixTreeNode::addMethods(const vector<string> &methods,
                              HandleFunc handler) {
  for (auto &m : methods) {
    if (this->methods.find(m) != this->methods.end() &&
        this->methods[m] != handler)
      return -1;
    this->methods[m] = handler;
  }
  return 0;
}

RadixTree::RadixTree() {
  this->root = make_shared<RadixTreeNode>();
}

int RadixTree::insert(const string &key, HandleFunc handler,
                      const vector<string> &methods) {
  auto root = this->root;
  auto i = 0UL, n = key.size();

  while (i < n) {
    auto children = root->children;
    auto empty = children.empty();
    auto end = children.end();

    if (children.find(ASTERISK) != end ||
        (key[i] == ASTERISK && !empty) ||
        (key[i] != COLON && children.find(COLON) != end) ||
        (key[i] == COLON && !empty && children.find(COLON) == end) ||
        (key[i] == COLON && children.find(COLON) != end && key.substr(
          i + 1, this->getpos(key.find(SLASH, i), n) - i - 1
          ) != children[COLON]->path)) {

      return -1;
    }

    if (root->children.find(key[i]) == root->children.end()) {
      auto p = key.find(COLON, i);

      if (p == string::npos) {
        p = key.find(ASTERISK, i);

        if (p == string::npos) {
          root = root->children[key[i]] = make_shared<RadixTreeNode>(
            key.substr(i));
          root->addMethods(methods, handler);
        } else {
          root = root->children[key[i]] = make_shared<RadixTreeNode>(
            key.substr(i, p - i));
          root = root->children[ASTERISK] = make_shared<RadixTreeNode>(
            key.substr(p + 1));
          root->addMethods(methods, handler);
        }
        return 0;
      }

      root = root->children[key[i]] = make_shared<RadixTreeNode>(
        key.substr(i, p - i));

      i = this->getpos(key.find(SLASH, p), n);
      root = root->children[COLON] = make_shared<RadixTreeNode>(
        key.substr(p + 1, i - p - 1));

      if (i == n)
        return root->addMethods(methods, handler);

    } else {
      root = root->children[key[i]];

      if (key[i] == COLON) {
        i += root->path.size() + 1;
        if (i == n)
          return root->addMethods(methods, handler);

      } else {
        auto j = 0UL, m = root->path.size();
        for (;i < n && j < m && key[i] == root->path[j]; ++i, ++j);

        if (j < m) {
          auto child = make_shared<RadixTreeNode>(root->path.substr(j));
          child->methods = root->methods;
          child->children = root->children;

          root->children = {{root->path[j], child}};
          root->path = root->path.substr(0, j);
          root->methods.clear();
        }

        if (i == n)
          return root->addMethods(methods, handler);
      }
    }
  }
  return 0;
}

ParseResult RadixTree::get(const string &key, const string &method) {
  unordered_map<string, string> params;

  auto root = this->root;
  auto i = 0UL, p = 0UL, n = key.size();

  while (i < n) {
    auto end = root->children.end();

    if (root->children.find(COLON) != end) {
      root = root->children[COLON];

      p = this->getpos(key.find(SLASH, i), n);
      params[root->path] = key.substr(i, p - i);
      i = p;
    } else if (root->children.find(ASTERISK) != end) {
      root = root->children[ASTERISK];
      params[root->path] = key.substr(i);
      break;
    } else if (root->children.find(key[i]) != end &&
        key.substr(i, root->children[key[i]]->path.size()) ==
        root->children[key[i]]->path) {
      root = root->children[key[i]];
      i += root->path.size();
    } else {
      return ParseResult();
    }
  }
  return ParseResult{true, root->methods[method], params};
}

}  // namespace radixtreee
