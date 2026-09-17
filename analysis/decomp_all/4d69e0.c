
void __fastcall FUN__text__004d69e0(int param_1)

{
  short sVar1;
  undefined3 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_58 [16];
  int local_18;
  undefined1 *local_14;
  short local_10;
  short local_c;
  int local_8;
  
  puVar4 = local_58;
  for (iVar3 = 0x15; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_10 = 0;
  local_8 = param_1;
  for (local_c = 0; local_c < 100; local_c = local_c + 1) {
    if (*(short *)(local_8 + 0x24 + local_c * 0x28) == 1) {
      local_10 = local_10 + 1;
      local_14 = (undefined1 *)(local_8 + 0x28 + local_c * 0x28);
      local_18 = (int)*(short *)(local_14 + 4);
      uVar2 = (undefined3)((uint)local_14 >> 8);
      switch(local_18) {
      case 0:
        FUN__text__004d2ba0(CONCAT31(uVar2,*local_14),(int)*(short *)(local_14 + 0x22),
                            (int)*(short *)(local_14 + 2),(int)*(short *)(local_14 + 0x1e),
                            (int)*(short *)(local_14 + 0x20));
        break;
      case 1:
        FUN__text__004d2ca0(CONCAT31(uVar2,*local_14),(int)*(short *)(local_14 + 0x22),
                            (int)*(short *)(local_14 + 2),(int)*(short *)(local_14 + 0x1e),
                            (int)*(short *)(local_14 + 0x20),(int)*(short *)(local_14 + 6),
                            (int)*(short *)(local_14 + 8),(int)*(short *)(local_14 + 0xe),
                            (int)*(short *)(local_14 + 0x10));
        break;
      case 2:
        FUN__text__004d2dd0(CONCAT31(uVar2,*local_14),(int)*(short *)(local_14 + 0x22),
                            (int)*(short *)(local_14 + 2),(int)*(short *)(local_14 + 0x1e),
                            (int)*(short *)(local_14 + 0x20),(int)*(short *)(local_14 + 6),
                            (int)*(short *)(local_14 + 8),(int)*(short *)(local_14 + 0xe),
                            (int)*(short *)(local_14 + 0x10),(int)*(short *)(local_14 + 0x12),
                            (int)*(short *)(local_14 + 0x14));
        break;
      case 3:
        FUN__text__004d3050(CONCAT31(uVar2,*local_14),(int)*(short *)(local_14 + 0x22),
                            (int)*(short *)(local_14 + 2),(int)*(short *)(local_14 + 0x1e),
                            (int)*(short *)(local_14 + 0x20),(int)*(short *)(local_14 + 6),
                            (int)*(short *)(local_14 + 8),(int)*(short *)(local_14 + 0xe),
                            (int)*(short *)(local_14 + 0x10),local_14[0x16],local_14[0x17],
                            local_14[0x18],local_14[0x19]);
        break;
      case 4:
        FUN__text__004d30c0(CONCAT31(uVar2,*local_14),(int)*(short *)(local_14 + 0x22),
                            (int)*(short *)(local_14 + 2),(int)*(short *)(local_14 + 0x1e),
                            (int)*(short *)(local_14 + 0x20),local_14[0x16],local_14[0x17],
                            local_14[0x18],local_14[0x19]);
      }
      *(short *)(local_8 + 0x26 + local_c * 0x28) = *(short *)(local_8 + 0x26 + local_c * 0x28) + 1;
      sVar1 = *(short *)(local_8 + 0x26 + local_c * 0x28);
      if (sVar1 == *(short *)(local_14 + 0x1a)) {
        FUN__text__004d6770(CONCAT22(sVar1 >> 0xf,local_c));
      }
    }
  }
  local_8 = 0x4d6c8f;
  FUN__text__0056ce80();
  return;
}

