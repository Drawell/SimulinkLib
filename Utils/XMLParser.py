from PySimCore import SimBaseClass, Environment, SimConnection, SimCompositeElement, SimBox
from Utils.Parser import Parser
import xml.etree.ElementTree as xml
import xml.etree.cElementTree as cxml


class XMLParser(Parser):
    @staticmethod
    def save(environment: Environment, path: str):
        root = xml.Element("root")
        main_env = xml.Element('MainEnvironment')
        root.append(main_env)
        #environment.cmp.save_to_xml(main_env)
        XMLParser._save_composite_element(environment.cmp, main_env)

        tree = xml.ElementTree(root)
        tree.write(path)

    @staticmethod
    def _save_composite_element(cmp: SimCompositeElement, parent):
        env_xml = xml.SubElement(parent, 'Environment')
        props_xml = xml.SubElement(env_xml, 'Properties')
        for key, value in cmp.properties.items():
            prop = xml.SubElement(props_xml, key)
            prop.text = str(value)

        for element in cmp.present_elements.values():
            XMLParser._save_element(element, env_xml)
            #element.save_to_xml(env_xml)

        for connection in cmp.present_connections:
            XMLParser._save_connection(connection, env_xml)
            #connection.save_to_xml(env_xml)

    @staticmethod
    def _save_element(element: SimBaseClass, parent):
        element_xml = xml.SubElement(parent, 'Element')
        element_xml.text = element.__class__.__name__

        props = xml.SubElement(element_xml, 'Properties')
        for key, value in element.properties.items():
            prop = xml.SubElement(props, key)
            prop.text = str(value)

    @staticmethod
    def _save_connection(connection: SimConnection, parent):
        connection_xml = xml.SubElement(parent, 'Connection')

        XMLParser._save_box(connection, connection_xml)
        #super().save_to_xml(connection_xml)

        start_socket_xml = xml.SubElement(connection_xml, 'StartSocket')
        if connection.input_socket is None:
            none_tag = xml.SubElement(start_socket_xml, 'None')
        else:
            name_xml = xml.SubElement(start_socket_xml, 'name')
            name_xml.text = connection.output_socket.parent_name
            index_xml = xml.SubElement(start_socket_xml, 'index')
            index_xml.text = str(connection.output_socket.index)

        end_socket_xml = xml.SubElement(connection_xml, 'EndSocket')
        if connection.input_socket is None:
            none_tag = xml.SubElement(end_socket_xml, 'None')
        else:
            name_xml = xml.SubElement(end_socket_xml, 'name')
            name_xml.text = connection.input_socket.parent_name
            index_xml = xml.SubElement(end_socket_xml, 'index')
            index_xml.text = str(connection.input_socket.index)

    @staticmethod
    def _save_box(box: SimBox, parent):
        box_xml = xml.SubElement(parent, 'SimBox')
        for key, value in box.properties.items():
            prop = xml.SubElement(box_xml, key)
            prop.text = str(value)

    @staticmethod
    def parse(path, import_directories: list)-> Environment:
        result_environment = Environment()
        for directory in import_directories:
            result_environment.import_classes_from_dir(directory)

        tree = cxml.ElementTree(file=path)

        root = tree.getroot()
        for child in root:
            print(child.tag, child.attrib)
            if child.tag == "MainEnvironment":
                XMLParser._parse_main_env(child, result_environment)
                #env_manager = EnvManager(env)

        return result_environment

    @staticmethod
    def _parse_main_env(main_env_xml, environment):
        env_xml = main_env_xml[0]
        if env_xml.tag != 'Environment':
            raise Exception('Filed to parse xml')

        for child in env_xml:
            if child.tag == 'Properties':
                prop = XMLParser._parse_properties(child)
                x = int(prop['x'])
                y = int(prop['y'])
                w = int(prop['width'])
                h = int(prop['height'])
                name = prop['name']
                environment.cmp = SimCompositeElement(x, y, name)
            elif child.tag == 'Element':
                XMLParser._parse_element(child, environment)
            elif child.tag == 'Connection':
                XMLParser._parse_connection(child, environment)

    @staticmethod
    def _parse_element(element, environment):
        class_name = element.text.strip()

        if class_name not in environment.imported_classes:
            raise Exception('Need to import class %s' % class_name)

        for prop_xml in element:
            if prop_xml.tag != 'Properties':
                raise Exception('Can not find properties for class %s' % class_name)

            prop = XMLParser._parse_properties(prop_xml)
            x = int(prop['x'])
            y = int(prop['y'])
            prop['width'] = int(prop['width'])
            prop['height'] = int(prop['height'])
            name = prop['name']
            environment.add_number_for_name_generation(class_name, int(name[len(class_name) + 1:]))
            environment.cmp.add_element(environment.imported_classes[class_name](**prop))
            break

    @staticmethod
    def _parse_connection(connection_xml, environment):
        for element in connection_xml:
            if element.tag == 'SimBox':
                prop = XMLParser._parse_properties(element)
                x = int(prop['x'])
                y = int(prop['y'])
                w = int(prop['width'])
                h = int(prop['height'])
                connection = SimConnection(environment.cmp, x, y, w, h)

            if element.tag == 'StartSocket':
                if element[0].tag != 'None':
                    prop = Environment.parse_properties(element)
                    name = prop['name']
                    index = int(prop['index'])
                    s = environment.cmp.get_socket(name, index)
                    connection.output_socket = s

                    if connection.input_socket is not None:
                        connection.output_socket.bind_with(connection.input_socket, connection)

            if element.tag == 'EndSocket':
                if element[0].tag != 'None':
                    prop = Environment.parse_properties(element)
                    name = prop['name']
                    index = int(prop['index'])
                    s = environment.cmp.get_socket(name, index)
                    connection.input_socket = s

                    if connection.output_socket is not None:
                        connection.output_socket.bind_with(connection.input_socket, connection)

        environment.cmp.add_connection(connection)

    @staticmethod
    def _parse_properties(parent_xml)-> dict:
        result = {}
        for prop in parent_xml:
            result[prop.tag] = prop.text
        return result
