library IEEE;
use IEEE.std_logic_1164.all;

entity HALFADDER is
    port (
        A, B     : in std_logic;
        S, C_out : out std_logic);
end HALFADDER;

architecture HA of HALFADDER is
begin -- Behavioral description
    S <= A xor B;
    C_out <= A and B;
end HA;