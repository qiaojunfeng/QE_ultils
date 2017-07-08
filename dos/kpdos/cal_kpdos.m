clear

f_par = 'par.k.pdos_tot';
f_per = 'per.k.pdos_tot';
% f_par = 'a.txt';

f = fopen(f_par);

nk_x = 20;
nk_y = 20;
nk_z = 1;
nkpt = nk_x*nk_y*nk_z;
sumpar_k = zeros(1,nkpt);
wk_k = ones(nkpt)./nkpt;

tline = fgetl(f);
tline = strtrim(fgetl(f));
ik = 1;
ndos = 0;
ndos_tot = -1;
while ischar(tline)
    tline = strtrim(tline);
    if ( ~ strcmp(tline, '') )
        tvec = strsplit(tline);
        e = str2double(tvec(2));
        if (ndos == 0)
            E_dw = e;
        elseif (ndos == (ndos_tot-1))
            E_up = e;
        end
        dos = str2double(tvec(3));
        sumpar_k(ik) = sumpar_k(ik) + e*dos*wk_k(ik);
        ndos = ndos + 1;
    else
        fprintf('ik = %i, ndos_tot = %i\n', ik, ndos)
        ndos_tot = ndos;
        ndos = 0;
        ik = ik + 1;
    end
    tline = fgetl(f);
end

fclose(f);

%%%

f = fopen(f_per);

sumper_k = zeros(1,nkpt);

tline = fgetl(f);
tline = strtrim(fgetl(f));
ik = 1;
ndos = 0;
while ischar(tline)
    tline = strtrim(tline);
    if ( ~ strcmp(tline, '') )
        tvec = strsplit(tline);
        e = str2double(tvec(2));
        dos = str2double(tvec(3));
        sumper_k(ik) = sumper_k(ik) + e*dos*wk_k(ik);
        ndos = ndos + 1;
    else
        fprintf('ik = %i, ndos_tot = %i\n', ik, ndos)
        ndos = 0;
        ik = ik + 1;
    end
    tline = fgetl(f);
end

fclose(f);

%%%

mae_k = sumpar_k - sumper_k;
% convert unit to meV
mae_k = mae_k * (E_up - E_dw) / ndos_tot * 1000;
mae = sum(mae_k)


% BOHR_RADIUS_ANGS= 0.52917720858999995;

% final unit probably is eV
% mae = mae * (1/BOHR_RADIUS_ANGS)^3

f_kpts = 'kpts';
f = fopen(f_kpts);

tline = strtrim(fgetl(f));
ik = 1;
mae_k_order = zeros(nk_x, nk_y);

while ischar(tline)
    tline = strtrim(tline);
    if ( ~ strcmp(tline, '') )
        tvec = strsplit(tline);
        kx = str2double(tvec(5));
        ky = str2double(tvec(6));
        iy = nk_x/2+1 + kx * nk_x;
        ix = nk_y/2+1 + ky * nk_y;
        mae_k_order(ix, iy) = mae_k(ik);
        ik = ik + 1;
    end
    tline = fgetl(f);
end

imagesc(mae_k_order);
colorbar
set(gca, 'YDir', 'normal')
xlabel('k_x')
ylabel('k_y')