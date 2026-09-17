
void FUN__text__0044e440(int param_1)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_150 [16];
  undefined1 local_110 [260];
  undefined4 local_c;
  undefined4 local_8;
  
  puVar3 = local_150;
  for (iVar2 = 0x53; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  FUN__text__0056d810(local_110,&DAT_00592b28,"data\\tactics\\map\\",
                      (&PTR_s_map00_vpt_006b13fc)[param_1 * 4]);
  uVar1 = FUN__text__004500b0(local_110);
  local_c = FUN__text__0044e4c0(uVar1);
  local_8 = 0x44e4ba;
  FUN__text__0056ce80();
  return;
}

