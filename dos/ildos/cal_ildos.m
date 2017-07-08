clear

n_x = 81;
n_y = 81;
n_z = 541;

% bohr
%L_x = 5.380370547;
%L_y = L_x;
%L_z = L_x * 6.268390298710899;

%delta_x = L_x/n_x*1000;
%delta_y = L_y/n_y*1000;
%delta_z = L_z/n_z*1000;

f = 'mae_ildos.xsf';
% f_par = 'a.txt';

%%%

f = fopen(f);

mae = 0;
iline = 0;
tline = fgetl(f);
while ischar(tline) 
    tvec = strsplit(strtrim(tline));
    mae = mae + sum(str2double(tvec));
    tline = fgetl(f);
    iline = iline + 1;
    fprintf('iline = %i\n', iline)
end

fclose(f);

%%%

%BOHR_RADIUS_ANGS = 0.52917720858999995;
RY_TO_EV = 13.605691930242388;

%mae = mae * (L_x*L_y*L_z);
mae = mae /(n_x*n_y*n_z)

% final unit is meV
mae = mae * 1000 * RY_TO_EV