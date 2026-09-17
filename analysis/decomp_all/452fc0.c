
void FUN__text__00452fc0(void)

{
  uint uVar1;
  int iVar2;
  short sVar4;
  uint uVar3;
  uint uVar5;
  undefined4 *puVar6;
  undefined8 uVar7;
  undefined4 local_60 [16];
  byte local_20;
  uint local_1c;
  int local_18;
  ushort local_14;
  ushort local_10;
  int local_c;
  int local_8;
  
  puVar6 = local_60;
  for (iVar2 = 0x17; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar6 = 0xcccccccc;
    puVar6 = puVar6 + 1;
  }
  FUN__text__00466b00(0x6e);
  uVar7 = FUN__text__00456b20();
  if ((int)uVar7 == 0) {
    if (DAT_007f448c._3_1_ == '\0') {
      FUN__text__00499c90(0,DAT_007f4492,DAT_007f4494,DAT_007f44a2,DAT_007f44a3,DAT_007f44a4);
    }
    else {
      FUN__text__00499c90(1,DAT_007f4492,DAT_007f4494,CONCAT31(DAT_007f448c._3_1_ >> 7,DAT_007f44a2)
                          ,DAT_007f44a3,DAT_007f44a4);
    }
    DAT_007f4505 = 1;
    DAT_007f4504 = 0;
  }
  else {
    uVar1 = (uint)DAT_007f4490;
    local_1c = (uint)(char)(&DAT_007f44f4)[uVar1];
    uVar3 = local_1c;
    uVar5 = (uint)((ulonglong)uVar7 >> 0x20);
    if (local_1c < 4) {
      sVar4 = (short)((char)(&DAT_007f44f4)[uVar1] >> 7);
      uVar5 = local_1c;
      switch(local_1c) {
      case 0:
        uVar1 = (uint)DAT_007f4492;
        local_10 = DAT_007f4492;
        uVar3 = CONCAT22(sVar4,DAT_007f4494);
        local_14 = DAT_007f4494;
        break;
      case 1:
        local_10 = DAT_007f4496;
        uVar1 = (uint)DAT_007f4498;
        local_14 = DAT_007f4498;
        uVar5 = CONCAT22(sVar4,DAT_007f4496);
        break;
      case 2:
        local_10 = DAT_007f449a;
        local_14 = DAT_007f449c;
        uVar3 = CONCAT22(sVar4,DAT_007f449a);
        uVar5 = CONCAT22(sVar4,DAT_007f449c);
        break;
      case 3:
        uVar1 = (uint)DAT_007f449e;
        local_10 = DAT_007f449e;
        local_14 = DAT_007f44a0;
        uVar3 = CONCAT22(sVar4,DAT_007f44a0);
      }
    }
    FUN__text__00499c90(0,local_10,CONCAT22((short)(uVar5 >> 0x10),local_14),
                        CONCAT31((int3)(uVar3 >> 8),DAT_007f44a2),
                        CONCAT31((int3)(uVar1 >> 8),DAT_007f44a3),
                        CONCAT31((int3)(uVar5 >> 8),DAT_007f44a4));
  }
  local_18 = (int)DAT_007f4488;
  FUN__text__0043a640(local_18);
  FUN__text__0043a920(local_18);
  FUN__text__0044e440(local_18);
  FUN__text__00467eb0();
  FUN__text__00466000();
  FUN__text__00451d80();
  FUN__text__0043a510();
  FUN__text__00451d80();
  if (DAT_007f448c._3_1_ == '\0') {
    if ((DAT_007f44b8 == '\0') || ((char)DAT_007f448c != '\0')) {
      for (local_c = 0; local_c != DAT_007f448c._1_1_; local_c = local_c + 1) {
      }
    }
    else {
      for (local_c = 0; local_c != DAT_007f448c._1_1_; local_c = local_c + 1) {
        if ((byte)(&DAT_007f45bc)[local_c * 0xb0] < 4) {
          (&DAT_007f4527)[local_c * 0xb0] = 1;
        }
      }
    }
  }
  else if ((char)DAT_007f448c == '\0') {
    for (local_c = 0; local_c != DAT_007f448c._1_1_; local_c = local_c + 1) {
      if ((byte)(&DAT_007f45bc)[local_c * 0xb0] < 4) {
        (&DAT_007f4527)[local_c * 0xb0] = 0;
      }
    }
  }
  else {
    for (local_c = 0; local_c != DAT_007f448c._1_1_; local_c = local_c + 1) {
      if ((byte)(&DAT_007f45bc)[local_c * 0xb0] < 4) {
        local_20 = (&DAT_007f4527)[local_c * 0xb0];
        if ((local_20 < 3) || (local_20 == 5)) {
          (&DAT_007f4527)[local_c * 0xb0] = 0;
        }
        if (((&DAT_007f4527)[local_c * 0xb0] != '\x04') &&
           (*(int *)(&DAT_007f453c + local_c * 0xb0) =
                 *(int *)(&DAT_007f453c + local_c * 0xb0) + 0x2a30,
           *(int *)(&DAT_007f4538 + local_c * 0xb0) < *(int *)(&DAT_007f453c + local_c * 0xb0))) {
          *(undefined4 *)(&DAT_007f453c + local_c * 0xb0) =
               *(undefined4 *)(&DAT_007f4538 + local_c * 0xb0);
        }
      }
    }
  }
  for (local_c = 0; local_c != DAT_007f448c._1_1_; local_c = local_c + 1) {
    if ((&DAT_007f45bc)[local_c * 0xb0] == DAT_007f4490) {
      FUN__text__0056d4d0(local_8 + 0xd0dbc + local_c * 0xb0,&DAT_007f4518 + local_c * 0xb0,0xb0);
      FUN__text__004680b0(local_c);
      FUN__text__00451d80();
    }
  }
  for (local_c = 0; local_c != DAT_007f448c._1_1_; local_c = local_c + 1) {
    if ((&DAT_007f45bc)[local_c * 0xb0] != DAT_007f4490) {
      FUN__text__0056d4d0(local_8 + 0xd0dbc + local_c * 0xb0,&DAT_007f4518 + local_c * 0xb0,0xb0);
      FUN__text__004680b0(local_c);
      FUN__text__00451d80();
    }
  }
  FUN__text__00453540();
  FUN__text__00468910();
  FUN__text__00467aa0(DAT_007f44a8);
  FUN__text__0041f710();
  FUN__text__00456b20();
  FUN__text__00422360(0);
  FUN__text__00415420();
  FUN__text__00422360(0);
  FUN__text__00415420();
  *(undefined4 *)(local_8 + 0x38) = 0;
  FUN__text__004077c0(DAT_007a49fc);
  local_8 = 0x453523;
  FUN__text__0056ce80();
  return;
}

