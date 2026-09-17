
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text__0045b9e0(void)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 uVar6;
  undefined8 uVar5;
  undefined4 local_304 [16];
  int local_2c4;
  int local_2c0;
  float local_2bc;
  float local_2b8;
  float local_2b4;
  float local_2b0;
  float local_2ac;
  int local_2a8;
  int local_2a4;
  undefined1 local_2a0 [512];
  int local_a0;
  uint local_9c;
  int local_98;
  undefined1 local_94 [88];
  undefined2 local_3c;
  int local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__0058fa1c;
  local_10 = ExceptionList;
  puVar4 = local_304;
  for (iVar3 = 0xbd; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  ExceptionList = &local_10;
  FUN__text__004075e0();
  local_8 = 0;
  local_9c = 0;
  local_a0 = 0;
  local_2a4 = 0;
  local_2a8 = -1;
  local_2ac = 0.0;
  local_2b0 = 0.0;
  local_2b4 = 512.0;
  local_2b8 = 384.0;
  local_2bc = 1.0;
  FUN__text__0056d810();
  FUN__text__00416370(0,0x40,0,local_2a0,0xffffffff);
  FUN__text__00422360();
  local_98 = FUN__text__00464d70(DAT_007a49fc,0);
  local_98 = FUN__text__00464de0();
  if ((local_98 != 0) &&
     (iVar3 = FUN__text__00424f80("ret==0","E:\\CrossHermit\\GAME\\src\\yoshida\\TestTask.cpp",
                                  DAT_0060ce94 + 0x17,0), iVar3 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  FUN__text__00409ef0();
  FUN__text__00464f80(local_14 + 0x1f10,0);
  while (iVar3 = FUN__text__004128f0(1,1), iVar3 == 0) {
    FUN__text__004077c0();
    local_3c = 1;
    FUN__text__0040a100();
    uVar6 = 0x80;
    uVar2 = __ftol();
    uVar5 = CONCAT44(uVar6,uVar2);
    uVar2 = __ftol(uVar2);
    FUN__text__0040a330(local_14 + 0x1f10,local_94,uVar2,uVar5);
    FUN__text__0056d810();
    FUN__text__00416370(0,0x20,0,local_2a0,0xffffffff);
    FUN__text__0056d810(local_2a0,&DAT_0059ac8c,(double)local_2bc);
    FUN__text__00416370(0,0x30,0,local_2a0,0xffffffff);
    FUN__text__0040b740();
    uVar2 = FUN__text__0040b6d0();
    FUN__text__0056d810(local_2a0,"ALLOC = %6d : FREE = %6d",uVar2);
    FUN__text__00416370(0,0x40,0,local_2a0,0xffffffff);
    if (local_9c == 0) {
      FUN__text__0056d810(local_2a0,&DAT_0059ac70);
    }
    else {
      FUN__text__0056d810(local_2a0,&DAT_0059ac54);
    }
    FUN__text__00416370(0,0x50,0,local_2a0,0xffffffff);
    FUN__text__0056d810(local_2a0,&DAT_0059ac40);
    FUN__text__00416370(0,0x60,0,local_2a0,0xffffffff);
    iVar3 = FUN__text__004128f0(200,2);
    if (iVar3 != 0) {
      local_a0 = local_a0 + 1;
    }
    iVar3 = FUN__text__004128f0(0xd0,2);
    if (iVar3 != 0) {
      local_a0 = local_a0 + -1;
    }
    iVar3 = FUN__text__004128f0(0x1c,1);
    if (iVar3 != 0) {
      FUN__text__00464f80(local_14 + 0x1f10,local_a0);
    }
    iVar3 = FUN__text__004128f0(0x39,1);
    if (iVar3 != 0) {
      local_9c = local_9c ^ 1;
    }
    local_2b0 = 0.0;
    local_2ac = 0.0;
    iVar3 = FUN__text__004128f0(0x50,0);
    if (iVar3 != 0) {
      local_2a4 = 2;
      local_2b0 = 1.0;
    }
    iVar3 = FUN__text__004128f0(0x4b,0);
    if (iVar3 != 0) {
      local_2a4 = 4;
      local_2ac = -1.0;
    }
    iVar3 = FUN__text__004128f0(0x4d,0);
    if (iVar3 != 0) {
      local_2a4 = 6;
      local_2ac = 1.0;
    }
    iVar3 = FUN__text__004128f0(0x48,0);
    if (iVar3 != 0) {
      local_2a4 = 8;
      local_2b0 = -1.0;
    }
    if (local_9c == 0) {
      iVar3 = FUN__text__004128f0(0x47,0);
      if (iVar3 != 0) {
        local_2a4 = 7;
        local_2ac = -1.0;
        local_2b0 = -1.0;
      }
      iVar3 = FUN__text__004128f0(0x4f,0);
      if (iVar3 != 0) {
        local_2a4 = 1;
        local_2ac = -1.0;
        local_2b0 = 1.0;
      }
      iVar3 = FUN__text__004128f0(0x49,0);
      if (iVar3 != 0) {
        local_2a4 = 9;
        local_2ac = 1.0;
        local_2b0 = -1.0;
      }
      iVar3 = FUN__text__004128f0(0x51,0);
      if (iVar3 != 0) {
        local_2a4 = 3;
        local_2ac = 1.0;
        local_2b0 = 1.0;
      }
    }
    else {
      if ((local_2ac == -1.0) && (local_2b0 == -1.0)) {
        local_2a4 = 7;
      }
      if ((local_2ac == -1.0) && (local_2b0 == 1.0)) {
        local_2a4 = 1;
      }
      if ((local_2ac == 1.0) && (local_2b0 == -1.0)) {
        local_2a4 = 9;
      }
      if ((local_2ac == 1.0) && (local_2b0 == 1.0)) {
        local_2a4 = 3;
      }
    }
    if ((local_2ac == _DAT_005924c0) && (local_2b0 == _DAT_005924c0)) {
      local_2c0 = local_2a8 + -1;
      switch(local_2c0) {
      case 0:
        FUN__text__00464f80(local_14 + 0x1f10,0xd);
        break;
      case 1:
        FUN__text__00464f80(local_14 + 0x1f10,9);
        break;
      case 2:
        FUN__text__00464f80(local_14 + 0x1f10,0xf);
        break;
      case 3:
        FUN__text__00464f80(local_14 + 0x1f10,10);
        break;
      case 5:
        FUN__text__00464f80(local_14 + 0x1f10,0xb);
        break;
      case 6:
        FUN__text__00464f80(local_14 + 0x1f10,0xc);
        break;
      case 7:
        FUN__text__00464f80(local_14 + 0x1f10,8);
        break;
      case 8:
        FUN__text__00464f80(local_14 + 0x1f10,0xe);
      }
      local_2a8 = -1;
    }
    if ((local_2ac != _DAT_005924c0) && (local_2b0 != _DAT_005924c0)) {
      if ((local_2ac == -1.0) && (local_2b0 == -1.0)) {
        local_2ac = -0.707;
        local_2b0 = -0.707;
      }
      if ((local_2ac == 1.0) && (local_2b0 == -1.0)) {
        local_2ac = 0.707;
        local_2b0 = -0.707;
      }
      if ((local_2ac == -1.0) && (local_2b0 == 1.0)) {
        local_2ac = -0.707;
        local_2b0 = 0.707;
      }
      if ((local_2ac == 1.0) && (local_2b0 == 1.0)) {
        local_2ac = 0.707;
        local_2b0 = 0.707;
      }
    }
    local_2ac = local_2ac * local_2bc;
    local_2b0 = local_2b0 * local_2bc;
    local_2b4 = local_2b4 + local_2ac;
    local_2b8 = local_2b8 + local_2b0;
    FUN__text__0056d810(local_2a0,"x = %f : y = %f",(double)local_2ac,(double)local_2b0);
    FUN__text__00416370(0,0x70,0,local_2a0,0xffffffff);
    if (((local_2ac != _DAT_005924c0) || (local_2b0 != _DAT_005924c0)) && (local_2a8 != local_2a4))
    {
      local_2a8 = local_2a4;
      local_2c4 = local_2a4 + -1;
      switch(local_2c4) {
      case 0:
        FUN__text__00464f80(local_14 + 0x1f10,0x1d);
        break;
      case 1:
        FUN__text__00464f80(local_14 + 0x1f10,0x19);
        break;
      case 2:
        FUN__text__00464f80(local_14 + 0x1f10,0x1f);
        break;
      case 3:
        FUN__text__00464f80(local_14 + 0x1f10,0x1a);
        break;
      case 5:
        FUN__text__00464f80(local_14 + 0x1f10,0x1b);
        break;
      case 6:
        FUN__text__00464f80(local_14 + 0x1f10,0x1c);
        break;
      case 7:
        FUN__text__00464f80(local_14 + 0x1f10,0x18);
        break;
      case 8:
        FUN__text__00464f80(local_14 + 0x1f10,0x1e);
      }
    }
    iVar3 = FUN__text__004128f0(0x2a,0);
    if (iVar3 == 0) {
      iVar3 = FUN__text__004128f0(0xd1,2);
      if (iVar3 != 0) {
        local_2bc = local_2bc - _DAT_0059ac28;
      }
      iVar3 = FUN__text__004128f0(0xc9,2);
      if (iVar3 != 0) {
        local_2bc = local_2bc + _DAT_0059ac28;
      }
    }
    else {
      iVar3 = FUN__text__004128f0(0xd1,2);
      if (iVar3 != 0) {
        local_2bc = local_2bc - _DAT_0059ac2c;
      }
      iVar3 = FUN__text__004128f0(0xc9,2);
      if (iVar3 != 0) {
        local_2bc = local_2bc + _DAT_0059ac2c;
      }
    }
    FUN__text__00422360();
  }
  FUN__text__00464d30();
  local_8 = 0xffffffff;
  FUN__text__00407710();
  ExceptionList = local_10;
  local_8 = 0x45c57d;
  FUN__text__0056ce80();
  return;
}

