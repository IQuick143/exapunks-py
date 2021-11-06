import dataclasses

from typing import List, Tuple

from construct import Struct, PrefixedArray, Array, PascalString
from construct import Byte, Int32ul, Const

"""
Special thanks to:
u/asterick
https://www.reddit.com/r/exapunks/comments/973luq/current_solution_file_format/

Solution format:

file_ver(?)	0x03ef
level_id	String
sol_name	String
comp_wins	int32
redshift_code_len	int32
win_count
win_stats()[
	win_struct{

	}
]
exa_len		int32
exa_list(exa_len)[
	exa_struct{
		unkn01		{0a}
		exa_name	String
		exa_code	String
		view_mode	int32
		m_mode		int32
		sprite		bool[100]
	}
]

String(length)[
	char: byte
]
"""

@dataclasses.dataclass
class WinValueBlock(object):
	valuepairs: List[Tuple[int, int]] = dataclasses.field(default_factory=list)

@dataclasses.dataclass
class Exa(object):
	name: str = "XA"
	code: str = ""
	view_mode: int = 0
	local_m_mode: bool = False
	bitmap: List[bool] = dataclasses.field(default_factory=lambda: [False] * 100)

class Solution(object):
	"""Class for savefile structures."""

	_solution_struct = Struct(
			Const(b"\xF0\x03\x00\x00"),
			'file_id' / PascalString(Int32ul, "utf8"),
			'solution_name' / PascalString(Int32ul, "utf8"),
			'competition_wins' / Int32ul,
			'redshift_code_len' / Int32ul,
			'wins' / PrefixedArray(Int32ul, Struct(
				'id' / Byte,
				'value' / Byte
			)),
			'exas' / PrefixedArray(Int32ul, Struct(
				Const(b"\x0A"),
				'name' / PascalString(Int32ul, "utf8"),
				'src_code' / PascalString(Int32ul, "utf8"),
				'view_mode' / Byte,
				'm_mode' / Byte,
				'bitmap' / Array(100, Byte)
			))
		)

	def __init__(self,
			file_id="PB000", solution_name="HELLO FROM EXAPUNKS DOT PY",
			exas:List[Exa] = list(), 
			competition_wins = 0, redshift_code_length = 0,
			wins: WinValueBlock = WinValueBlock()
		):
		"""Constructor.
		"""
		self.file_id=file_id
		self.solution_name=solution_name
		self.exas=exas
		self.competition_wins=competition_wins
		self.redshift_code_length=redshift_code_length
		self.wins=wins

	@staticmethod
	def from_bytes(solution_data: bytes):
		"""Construct a Solution object from the binary representation.

		Args:
			solution_data: Binary representation in the save file.
		
		Returns:
			Parsed Solution object.
		"""
		
		parsed_struct = Solution._solution_struct.parse(solution_data)
		exas = []
		for x in parsed_struct.exas:
			exas.append(
				Exa(
					name=x.name,
					code=x.src_code,
					view_mode=x.view_mode,
					local_m_mode=x.m_mode,
					bitmap=x.bitmap
				)
			)
		return Solution(
			file_id=parsed_struct.file_id,
			solution_name=parsed_struct.solution_name,
			exas=exas,
			competition_wins=parsed_struct.competition_wins,
			redshift_code_length=parsed_struct.redshift_code_len,
			wins=WinValueBlock(valuepairs=[(win.id, win.value) for win in parsed_struct.wins])
		)
	
	@staticmethod
	def from_file(filename):
		"""Construct a solution from an exapunks .solution binary file

		Args:
			filename: path to the file

		Returns:
			Parsed Solution object.
		"""
		with open(filename, 'br') as file:
			return Solution.from_bytes(file.read())

	def to_file(self, filename):
		"""Write a solution to a .solution binary file

		Args:
			filename: path to the file

		Returns:
		"""
		with open(filename, 'bw') as file:
			file.write(bytes(self))
	
	def update_metadata(self):
		"""Recalculates metadata like redshift_code_length
		"""
		line_count = 0
		for exa in self.exas:
			for line in exa.code.split("\n"):
				if len(line) > 0 and not line.startswith("NOTE") and not line.startswith("DATA") and not line.strip().startswith(";"):
					line_count += 1
		
		self.redshift_code_length = line_count
	
	# Magic methods:
	
	def __bytes__(self):
		return Solution._solution_struct.build({
			'file_id': self.file_id,
			'solution_name': self.solution_name,
			'competition_wins': self.competition_wins,
			'redshift_code_len': self.redshift_code_length,
			'wins': [{'id':pair[0], 'value':pair[1]} for pair in self.wins.valuepairs],
			'exas': [{
				'name': exa.name,
				'src_code': exa.code,
				'view_mode': exa.view_mode,
				'm_mode': exa.local_m_mode,
				'bitmap': exa.bitmap
			} for exa in self.exas]
		})
