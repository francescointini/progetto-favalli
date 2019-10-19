library ieee;
use ieee.std_logic_1164.all;

entity HALFADDER_TB is
end HALFADDER_TB;

architecture HA_TB of HALFADDER_TB is
	signal A_SGN : std_logic;
	signal B_SGN : std_logic;
	signal S_SGN : std_logic;
	signal C_OUT_SGN : std_logic;

	component HALFADDER is
	port (
		A, B : in std_logic,
		S, C_OUT : out std_logic);
	end component;
begin
	HA : HALFADDER port map ( A_SGN, B_SGN, S_SGN, C_OUT_SGN )

	HA_TB : process
		QUI VANNO I PROCESSI
