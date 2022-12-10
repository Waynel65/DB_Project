use FlaskDemo;

-- insertions for unit table
INSERT INTO Unit (unitName) values ('ml');
INSERT INTO Unit (unitName) values ('fl oz');
INSERT INTO Unit (unitName) values ('g');
INSERT INTO Unit (unitName) values ('oz');
INSERT INTO Unit (unitName) values ('mm');
INSERT INTO Unit (unitName) values ('inch');


-- insertions for UnitConversion table
INSERT INTO UnitConversion (sourceUnit, destinationUnit, ratio) values ('ml', 'fl oz', 0.034)
INSERT INTO UnitConversion (sourceUnit, destinationUnit, ratio) values ('fl oz', 'ml', 29.57)
INSERT INTO UnitConversion (sourceUnit, destinationUnit, ratio) values ('g', 'oz', 0.0035)
INSERT INTO UnitConversion (sourceUnit, destinationUnit, ratio) values ('oz', 'g', 28.35)
INSERT INTO UnitConversion (sourceUnit, destinationUnit, ratio) values ('mm', 'inch', 0.039)
INSERT INTO UnitConversion (sourceUnit, destinationUnit, ratio) values ('inch', 'mm', 29.5)