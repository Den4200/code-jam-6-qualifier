# KVLang is a yaml-inspired declarative language to describe user
# interfaces you can find an introduction to its syntax here
# https://kivy.org/doc/stable/guide/lang.html

# for an even shorter introduction…
# Widgets are declared nested by indentation, and properties are
# similarly defined in the scope (indentation level) of the widget they
# apply to. It also allows defining canvas (graphical) instructions much
# in the same way as widgets.

# KVlang also allows declaring "rules" for widget classes, these rules
# will similarly declare a tree of widget children, properties and
# canvas instructions, that will be automatically applied to all
# instances of these classes, these rules are declared using the class
# name around pointy brackets, e.g: "<MyCustomLabel>:" would declare a
# rule applied to all instances of the MyCustomLabel class (which you
# could define as a subclass of kivy.uix.label.Label).

# The string can contain at most one "root" rule, which is a rule
# without <> around its name, this rule is treated differently, it
# directly instantiates a widget of the class, and adds the declared
# properties, graphical instructions and children widgets to it. This
# widget is returned by the Builder.load_string (or Builder.load_file)
# call, so it can be added to the widget tree, either as root, or to an
# existing parent widget of your choice. In the example below, "Label"
# is the "root rule".
