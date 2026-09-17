
void __thiscall FUN__text__00410b10(int param_1,undefined2 param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (*(int *)(param_1 + 0x44) != 0) {
    local_10 = *(int *)(param_1 + 0x4c);
    local_8 = param_1;
    if (local_10 == 0) {
      local_c = CONCAT31(local_c._1_3_,(char)((uint)*(undefined4 *)(param_1 + 0x58) >> 0x10));
      FUN__text__00410310(0,0,0x403,0x300,param_2,local_c << 0x18,1);
    }
    else if (local_10 == 1) {
      local_c = CONCAT31(local_c._1_3_,(char)((uint)*(undefined4 *)(param_1 + 0x58) >> 0x10));
      FUN__text__00410310(0,0,0x403,0x300,param_2,
                          CONCAT31((uint3)(CONCAT22((short)((uint)(local_c << 0x18) >> 0x10),0xff00)
                                          >> 8) | 0xff00,0xff),1);
    }
    else {
      iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\src\\system\\directx\\DxDraw.cpp",
                                  DAT_005ff368 + 0xd,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
  }
  local_8 = 0x410c12;
  FUN__text__0056ce80();
  return;
}

