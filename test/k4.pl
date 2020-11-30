vua(dat).
thuoc_ha(kien,dat).
thuoc_ha(hari,dat).
thuoc_ha(thuy_tien,dat).
thuoc_ha(hai,dat).
thuoc_ha(thanh,dat).
thuoc_ha(phu,dat).
thuoc_ha(viet,dat).
thuoc_ha(viet,phu).
thuoc_ha(trong,dat).
thuoc_ha(dang,dat).
thuoc_ha(quan,dat).

con_trai(kien,dat).
con_trai(thanh,hai).
con_gai(hari,dat).
con_gai(thuy_tien,dat).

co_tai(quan).
co_tai(hai).
co_tai(phu).
khong_co_tai(trong).

thich_khach(viet,dat).

ket_hon(thanh,hari).
ket_hon(hari,thanh).
ket_hon(thuy_tien,cong_vinh).

vua(hieu).
thuoc_ha(cong_vinh,hieu).
thuoc_ha(thuy_tien,hieu).
thuoc_ha(quynh,hieu).
thuoc_ha(vuong,hieu).
thuoc_ha(hoang,hieu).
thuoc_ha(nguyen,hieu).
thuoc_ha(quan,hieu).

co_tai(cong_vinh).
co_tai(vuong).
khong_co_tai(nguyen).

con_trai(cong_vinh,hieu).
con_gai(quynh,hieu).
con_trai(hoang,vuong).

ket_hon(hoang,quynh).
ket_hon(cong_vinh,thuy_tien).


vua(son).
thuoc_ha(khoa,son).
thuoc_ha(minh,son).
thuoc_ha(minh,khoa).
thuoc_ha(dang,son).
thuoc_ha(nien,son).
thuoc_ha(nien,dang).
thuoc_ha(phu,son).

co_tai(khoa).
co_tai(dang).

thich_khach(nien,son).
thich_khach(minh,son).



thai_giam(Nguoi,Vua):-thuoc_ha(Nguoi,Vua), vua(Vua), khong_co_tai(Nguoi).
quan(Nguoi,Vua):- thuoc_ha(Nguoi,Vua), vua(Vua), co_tai(Nguoi).
hoang_tu(Nguoi,Vua):- con_trai(Nguoi,Vua), vua(Vua).
hoang_thai_tu(Nguoi,Vua):- hoang_tu(Nguoi,Vua), co_tai(Nguoi).
cong_chua(Nguoi,Vua) :- con_gai(Nguoi,Vua), vua(Vua).

hoang_tu_phi(Nguoi,Vua):- ket_hon(Nguoi,HoangTu), hoang_tu(HoangTu,Vua).
hoang_thai_tu_phi(Nguoi,Vua):- ket_hon(Nguoi,HoangThaiTu), hoang_thai_tu(HoangThaiTu,Vua).
pho_ma(Nguoi,Vua) :- ket_hon(Nguoi,CongChua), cong_chua(CongChua,Vua).
phan_quoc(Quan,Vua) :- quan(Quan,Vua), thuoc_ha(ThuocHa,Quan), thich_khach(ThuocHa,Vua).

noi_gian(Quan,Vua1,Vua2) :- thuoc_ha(Quan,Vua1), vua(Vua1), phan_quoc(Quan, Vua2).
dong_minh(Vua1,Vua2) :- cong_chua(CongChua, Vua1), hoang_tu(HoangTu, Vua2),  ket_hon(HoangTu, CongChua).
ke_thu(Vua1, Vua2) :- thuoc_ha(Quan,Vua1), noi_gian(Quan,Vua1,Vua2).
su_gia(Quan, Vua1, Vua2) :- quan(Quan,Vua1), thuoc_ha(Quan,Vua2), dong_minh(Vua1,Vua2).
