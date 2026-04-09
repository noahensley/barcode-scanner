# barcode-scanner
***
Requirements
***
1. The software shall run on a client laptop.
2. The software shall run on the client’s laptop command line interface (CLI)
3. The software shall use a built-in or external webcam to capture a moving image (sequence of n images).
4. After an attempted decoding, n captured images shall be deleted.
5. The sequence of images shall be saved inside an intermediate directory alongside the program directory.
6. The software shall provide the user with a continuous feed of what the webcam is seeing in a separate window to assist the user in placing the barcode within the bounds of the webcam.
7. The software shall attempt to decode each image in the sequence as a one of the supported barcode types. If the decode is unsuccessful, it shall repeat the process for the next supported barcode type until a successful   decoding occurs.
8. The software shall spport barcode types: UPC-A, UPC-E, EAN-8, and EAN-13.
9. The software shall produce a successfully decoded number as output to the CLI.
10. A successful decode shall be considered any moving image analysis that results in an output sequence of digits.
11. A successful read shall be considered an output number that matches the physical number on the barcode.
12. The software shall notify the user of an unsuccessful decode via a CLI error message and an error sound.
13. An unsuccessful decode shall be considered any image that the program is unable to recognize as a supported barcode
14. The software shall have a successful read rate of 95% 
15. Verified through manual testing by the development team before shipment.
16. An unsuccessful read shall be considered an output that does not match the physical number on the barcode.
17. Success rate shall be determined by the amount of unsuccessful versus successful reads during a series of tests
