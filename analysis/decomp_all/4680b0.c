
void __thiscall FUN__text__004680b0(int param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_64 [16];
  undefined4 local_24;
  undefined4 local_20;
  undefined4 local_1c;
  int local_18;
  short *local_14;
  uint local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_64;
  for (iVar2 = 0x18; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = param_2;
  local_8 = param_1;
  if (((param_2 < 0) || (0xf9 < param_2)) &&
     (iVar2 = FUN__text__00424f80("(0<=uno) && (uno<(250))",
                                  "E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                  DAT_00618b48 + 6,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_14 = (short *)(local_8 + 0x80aec + local_c * 0x520);
  if ((*local_14 != 0) &&
     (iVar2 = FUN__text__00424f80("wk->used == 0",
                                  "E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                  DAT_00618b48 + 9,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  _memset(local_14,0,0x520);
  *local_14 = 1;
  local_14[1] = (short)local_c;
  *(undefined1 *)(local_14 + 4) = 0;
  local_14[0x286] = 0;
  *(int *)(local_14 + 300) = local_8 + 0xd0c2c + local_c * 0xb0;
  local_18 = *(int *)(local_14 + 300);
  local_10 = (uint)*(ushort *)(local_18 + 0xc);
  *(undefined1 *)((int)local_14 + 0x501) = 0xff;
  local_14[0x12e] = 0;
  local_14[0x12f] = 0;
  FUN__text__0046c040(local_14,2);
  *(undefined1 *)((int)local_14 + 0x28b) = 2;
  *(undefined2 *)(*(int *)(local_14 + 300) + 0xa6) = 0xffff;
  *(undefined2 *)(*(int *)(local_14 + 300) + 0xa8) = 0;
  *(undefined2 *)(*(int *)(local_14 + 300) + 0xaa) = 0;
  *(undefined2 *)(*(int *)(local_14 + 300) + 0xac) = 0;
  *(undefined1 *)(*(int *)(local_14 + 300) + 0xae) = 0;
  FUN__text__00474fb0(local_14);
  FUN__text__004750b0(local_14);
  if (*(char *)(*(int *)(local_14 + 300) + 0xf) == '\x01') {
    iVar2 = FUN__text__00468eb0(local_14);
    if (iVar2 == 0) {
      FUN__text__00475370(local_14,2,0xffffffff);
    }
    else {
      FUN__text__00475370(local_14,0x19,0xffffffff);
    }
  }
  else {
    FUN__text__00475370(local_14,0xb,0xffffffff);
  }
  local_14[0x277] = -1;
  FUN__text__00467020(local_14,local_10);
  *(undefined1 *)((int)local_14 + 0x4e7) = 0xff;
  *(undefined1 *)(local_14 + 0x274) = 0xff;
  FUN__text__00468690(local_14,*(undefined1 *)(local_18 + 0x9b),*(undefined1 *)(local_18 + 0x9c));
  *(undefined1 *)((int)local_14 + 0x4e9) = *(undefined1 *)((int)local_14 + 0x4e7);
  *(char *)(local_14 + 0x275) = (char)local_14[0x274];
  local_14[0x266] = 0;
  local_14[0x267] = 0;
  local_14[0x268] = local_14[0x266];
  local_14[0x269] = local_14[0x267];
  *(undefined1 *)(local_14 + 0x174) = *(undefined1 *)((int)local_14 + 0x4e7);
  *(char *)((int)local_14 + 0x2e9) = (char)local_14[0x274];
  *(undefined1 *)((int)local_14 + 0x4e5) = 0xff;
  *(undefined1 *)(local_14 + 0x273) = 0xff;
  FUN__text__00480f50(local_14);
  FUN__text__00437c90(local_14 + 0x17a);
  FUN__text__00437c90(local_14 + 0x1f0);
  iVar2 = FUN__text__00468d80(local_14);
  if (iVar2 == 0) {
    local_14[0x27f] = 600;
  }
  else {
    local_14[0x27f] = 900;
  }
  FUN__text__00466fc0(local_14);
  FUN__text__00492e60(local_14 + 0x27c);
  FUN__text__00492e60(local_14 + 0x27d);
  FUN__text__00492e60(local_14 + 0x27e);
  iVar2 = FUN__text__00469ad0(local_14);
  if (iVar2 == 0) {
    iVar2 = FUN__text__00469b90(local_14);
    if (iVar2 == 0) {
      iVar2 = FUN__text__00469c60(local_14);
      if (iVar2 == 0) {
        iVar2 = FUN__text__00468d80(local_14);
        if (iVar2 == 0) {
          FUN__text__0046c040(local_14,2);
        }
      }
      else {
        local_24 = FUN__text__0046a950(local_14);
        switch(local_24) {
        case 0:
          FUN__text__0046c040(local_14,2);
          break;
        case 1:
          FUN__text__0046c040(local_14,4);
          break;
        case 2:
          FUN__text__0046c040(local_14,7);
          break;
        case 3:
          FUN__text__0046c040(local_14,2);
          break;
        case 4:
          FUN__text__0046c040(local_14,1);
        }
        FUN__text__00475370(local_14,0x1c,1);
        *(undefined1 *)(*(int *)(local_14 + 300) + 0x9f) = 2;
      }
    }
    else {
      local_20 = FUN__text__0046a950(local_14);
      switch(local_20) {
      case 0:
        FUN__text__0046c040(local_14,2);
        break;
      case 1:
        FUN__text__0046c040(local_14,4);
        break;
      case 2:
        FUN__text__0046c040(local_14,7);
        break;
      case 3:
        FUN__text__0046c040(local_14,2);
        break;
      case 4:
        FUN__text__0046c040(local_14,1);
      }
      FUN__text__00475370(local_14,0x1c,1);
    }
  }
  else {
    local_1c = FUN__text__0046a950(local_14);
    switch(local_1c) {
    case 0:
      FUN__text__0046c040(local_14,2);
      break;
    case 1:
      FUN__text__0046c040(local_14,4);
      break;
    case 2:
      FUN__text__0046c040(local_14,7);
      break;
    case 3:
      FUN__text__0046c040(local_14,2);
      break;
    case 4:
      FUN__text__0046c040(local_14,1);
    }
    *(undefined1 *)(*(int *)(local_14 + 300) + 0x9f) = 2;
  }
  local_8 = 0x46863f;
  FUN__text__0056ce80();
  return;
}

