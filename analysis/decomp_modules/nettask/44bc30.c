
void __fastcall FUN__text__0044bc30(int param_1)

{
  char cVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_64 [16];
  short local_24;
  short local_20;
  short local_1c;
  short local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_64;
  for (iVar2 = 0x18; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = param_1 + 0x1a54;
  local_20 = 0;
  local_24 = 0;
  if (*(char *)(param_1 + 0x1a8b) == '\x01') {
    *(undefined1 *)(param_1 + 0x9c) = 0x68;
    *(undefined1 *)(param_1 + 0x9d) = 0x68;
    *(undefined1 *)(param_1 + 0x9e) = 0x68;
  }
  else {
    *(undefined1 *)(param_1 + 0x9c) = 0x80;
    *(undefined1 *)(param_1 + 0x9d) = 0x80;
    *(undefined1 *)(param_1 + 0x9e) = 0x80;
  }
  local_8 = param_1;
  for (local_10 = 0; local_10 != 4; local_10 = local_10 + 1) {
    cVar1 = *(char *)(local_c + local_10 + 0x38);
    local_14 = (int)cVar1;
    local_18 = local_20 + *(short *)(&DAT_006065e0 + (local_10 * 5 + local_14) * 8);
    local_1c = local_24 + *(short *)(&DAT_006065e2 + (local_10 * 5 + local_14) * 8);
    FUN__text__0044cb40(local_8 + 0x38,CONCAT22(cVar1 >> 7,local_18),
                        CONCAT22(*(short *)(&DAT_006065e2 + (local_10 * 5 + local_14) * 8) >> 0xf,
                                 local_1c),0x55,5,&DAT_00606680 + local_14 * 8);
  }
  *(undefined1 *)(local_8 + 0x9c) = 0x80;
  *(undefined1 *)(local_8 + 0x9d) = 0x80;
  *(undefined1 *)(local_8 + 0x9e) = 0x80;
  local_8 = 0x44bd61;
  FUN__text__0056ce80();
  return;
}

