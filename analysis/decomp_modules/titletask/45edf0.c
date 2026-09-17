
void __fastcall FUN__text__0045edf0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  undefined4 local_18;
  undefined4 local_14;
  undefined4 local_10;
  undefined4 local_c;
  int local_8;
  
  puVar2 = local_58;
  for (iVar1 = 0x15; local_8 = param_1, iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  do {
    local_10 = *(undefined4 *)(local_8 + 0x30);
    switch(local_10) {
    case 0:
      FUN__text__004db060(0x20,0);
      FUN__text__0045f0d0();
      *(undefined4 *)(local_8 + 0x30) = 1;
      break;
    case 1:
      local_14 = FUN__text__0045efb0();
      local_c = local_14;
      switch(local_14) {
      case 0:
      case 1:
      case 4:
        *(undefined4 *)(local_8 + 0x30) = 0x14;
        break;
      case 2:
        *(undefined4 *)(local_8 + 0x30) = 10;
        break;
      case 3:
      case 5:
        *(undefined4 *)(local_8 + 0x30) = 0x14;
        break;
      case 6:
        *(undefined4 *)(local_8 + 0x30) = 0x14;
      }
      break;
    case 10:
      iVar1 = FUN__text__0045f3d0();
      if (iVar1 == 0) {
        *(undefined4 *)(local_8 + 0x30) = 0x14;
      }
      else {
        *(undefined4 *)(local_8 + 0x30) = 1;
      }
      break;
    case 0x14:
      FUN__text__0045f310();
      local_18 = local_c;
      switch(local_c) {
      case 0:
      case 1:
      case 2:
      case 3:
      case 4:
      case 6:
LAB__text__0045eefe:
        FUN__text__004db230(0x5a);
        while (iVar1 = FUN__text__004db270(), iVar1 == 0) {
          FUN__text__00422360(0);
        }
        FUN__text__004db300();
        FUN__text__00422360(0);
        local_8 = 0x45ef42;
        FUN__text__0056ce80();
        return;
      case 5:
        goto LAB__text__0045eefe;
      }
    }
  } while( true );
}

