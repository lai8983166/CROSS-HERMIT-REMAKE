
/* WARNING: Removing unreachable block (ram,0x004de0cd) */

void FUN__text__004ddf40(undefined4 param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  int local_14;
  byte *local_10;
  undefined *local_c;
  undefined4 local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if ((100 < param_2) &&
     (iVar2 = FUN__text__00424f80("skill <= (100)","E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp"
                                  ,DAT_00738c9c + 6,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_c = &DAT_006c2dc8 + param_2 * 0x48;
  local_10 = (byte *)FUN__text__004de8f0(param_2);
  local_14 = *local_10 - 2;
  switch(local_14) {
  case 0:
    break;
  case 1:
    break;
  case 2:
    break;
  case 3:
  }
  local_8 = 0x4de0e4;
  FUN__text__0056ce80();
  return;
}

