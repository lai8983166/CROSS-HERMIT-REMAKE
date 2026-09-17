
void __fastcall FUN__text__00463450(int param_1)

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
LAB__text__0046346d:
  local_10 = *(undefined4 *)(local_8 + 0x30);
  switch(local_10) {
  case 0:
    FUN__text__004db060(0x20,0);
    FUN__text__004637e0();
    *(undefined4 *)(local_8 + 0x30) = 1;
    break;
  case 1:
    local_14 = FUN__text__004636c0();
    local_c = local_14;
    switch(local_14) {
    case 0:
    case 1:
    case 4:
    case 5:
    case 6:
    case 7:
    case 8:
      *(undefined4 *)(local_8 + 0x30) = 0x14;
      break;
    case 2:
      *(undefined4 *)(local_8 + 0x30) = 10;
      break;
    case 3:
      *(undefined4 *)(local_8 + 0x30) = 0x14;
    }
    break;
  case 10:
    iVar1 = FUN__text__00463ae0();
    if (iVar1 == 0) {
      *(undefined4 *)(local_8 + 0x30) = 0x14;
    }
    else {
      *(undefined4 *)(local_8 + 0x30) = 1;
    }
    break;
  case 0x14:
    FUN__text__00463a20();
    local_18 = local_c;
    switch(local_c) {
    case 0:
    case 1:
    case 2:
    case 4:
    case 5:
    case 6:
    case 7:
    case 8:
      FUN__text__004db230(0x5a);
      while (iVar1 = FUN__text__004db270(), iVar1 == 0) {
        FUN__text__00422360(0);
      }
      FUN__text__004db300();
      FUN__text__00422360(0);
      local_8 = 0x463654;
      FUN__text__0056ce80();
      return;
    case 3:
      FUN__text__00463da0(3);
      FUN__text__00463d20(3);
      FUN__text__00463e60(3);
      FUN__text__00463da0(4);
      FUN__text__00463d20(4);
      FUN__text__00463e60(4);
      FUN__text__00463da0(5);
      FUN__text__00463d20(5);
      FUN__text__00463e60(5);
      FUN__text__00463da0(7);
      FUN__text__00463d20(7);
      FUN__text__00463e60(7);
      FUN__text__00463da0(8);
      FUN__text__00463d20(8);
      FUN__text__00463e60(8);
      FUN__text__00463970();
      *(undefined4 *)(local_8 + 0x30) = 1;
      break;
    default:
      goto switchD__text__00463498_caseD_2;
    }
    goto LAB__text__0046346d;
  }
switchD__text__00463498_caseD_2:
  goto LAB__text__0046346d;
}

