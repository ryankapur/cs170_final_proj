import sys

def write():
	edges1 = [(1, 12), (12, 128), (25, 76), (25, 120), (37, 250), (47, 225), (52, 76), \
	(52, 37), (54, 12), (54, 1), (54, 25), (76, 54), (120, 225), (120, 47), (120, 52), (128, 12), \
	(128, 52), (128, 76),  (225, 276), (250, 47), (276, 25), (276, 120), (225, 281), (281, 282), (282, 283), \
	(283, 284), (284, 285), (285, 286), (286, 287), (276, 66), (66, 77), (77, 110), (110, 66), (77, 88), (88, 99), (99, 110)]

	edges2 = [(54, 102), (102, 72), (72, 137), (72, 7), (137, 98), (98, 11), (98, 99), (98, 194), \
	(98, 7), (72, 7), (7, 108), (108, 77), (77, 181), (181, 108), (190, 27), (27, 21), (21, 190), (182, 189), \
	(189, 160), (160, 173), (173, 182), (40, 84), (11, 128), (128, 93), (93, 5), (5, 112), (112, 163), (163, 196), \
	(196, 51), (51, 52), (52, 87), (87, 134), (134, 144), (144, 36), (36, 12), (12, 22), (22, 161), (161, 159), (159, 83), \
	(83, 64), (64, 95), (95, 114), (99, 119), (119, 6), (6, 185), (185, 146), (146, 199), (199, 2), (2, 81), (81, 80), (80, 70), \
	(70, 179), (179, 135), (135, 20), (20, 96), (96, 38), (38, 47), (47, 88), (88, 152), (152, 129), (129, 171), (171, 130), \
	(194, 76), (76, 44), (44, 4), (4, 103), (103, 55), (55, 30), (30, 104), (104, 3), (3, 15), (15, 34), (34, 101), (101, 10), (10, 35), \
	(35, 191), (191, 165), (165, 43), (43, 123), (123, 53), (53, 82), (82, 33), (113, 39), (39, 57), (57, 172), (172, 176), (176, 74), (74, 42), \
	(42, 148), (148, 156), (156, 193), (193, 18), (18, 118), (118, 31), (31, 150), (150, 71), (71, 66), (66, 116), (116, 124), \
	(124, 170), (170, 155), (155, 167), (167, 16), (16, 157), (157, 49), (49, 186), (186, 149), (149, 117), (117, 8), (8, 28), (28, 26), (26, 50)]

	edges3 = [ (81,39), (68,81), (6,81) , (67, 81), (67, 27) , \
	(6, 27), (6, 68), (18, 68), (73, 25), (25, 41), (41, 67), (67, 21), (6,73), (7, 63), \
	(63, 40), (40, 18), (6, 99), (70, 99), (48, 27), (70, 48), (48, 69), (17, 70), (70, 62), (62, 17),\
	 (27, 62), (99, 39), (39, 66), (39, 10), (66, 10), (42, 10), (14, 20), (20, 14), (13, 26), (26, 37), (37, 61), \
	 ( 61, 38), (61, 38), (61, 31), (31, 13), (31, 72), (31, 30), (72, 15),  (29, 15), (30, 15), (31, 29), (15, 65), \
	 (65, 38), (38, 24), (24, 9),  (9, 23), (27, 21), (38, 22), (64, 24), (19, 92), (38, 19), (31, 28), (37, 9), (19, 28), (92, 94), \
	 (92, 95), (28, 91), (94, 8), (95, 8), (95, 71), (64, 11), (11, 9), (11, 23)]
	 
	try:
		print("Hi I want to make you graph")
		f1 = open("BITScrastinators1.in", "w")
		f2 = open("BITScrastinators2.in", "w")
		f3 = open("BITScrastinators3.in", "w")
		f1.write("288\n1 25 76 77 120 276\n")
		f2.write("200\n11 99 194 40 84\n")
		f3.write("160\n67 6 68 70 19 28 24\n")
		s1 = ""
		s2 = ""
		s3 = ""
		written = False
		for x in range(288):
			for y in range(288):
				for edge in edges1:
					if x == edge[0] and y == edge[1] and not written:
						s1 = s1 + "1 "
						written = True
				if not written:
					s1 = s1 + "0 "
				written = False
			s1 = s1 + "\n"
			f1.write(s1)
			s1 = ""
		written = False
		for x in range(200):
			for y in range(200):
				for edge in edges2:
					if x == edge[0] and y == edge[1] and not written:
						written = True
						s2 = s2 + "1 "
				if not written:
					s2 = s2 + "0 "
				written = False
			s2 = s2 + "\n"
			f2.write(s2)
			s2 = ""
		written = False
		for x in range(160):
			for y in range(160):
				for edge in edges3:
					if x == edge[0] and y == edge[1] and written:
						s3 = s3 + "1 "
						written = True
				if not written:
					s3 = s3 + "0 "
				written = False
			s3 = s3 + "\n"
			f3.write(s3)
			s3 = ""
		f1.close()
		f2.close()
		f3.close()
	except Exception as e:
		print('error: {0}'.format(e))
write()
print("Made your graph, goodbye")