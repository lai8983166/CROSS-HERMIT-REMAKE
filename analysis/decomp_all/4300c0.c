
/* WARNING: Removing unreachable block (ram,0x004301f4) */

void __fastcall FUN__text__004300c0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  undefined4 local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; local_8 = param_1, iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  do {
    local_c = *(undefined4 *)(local_8 + 0x30);
    switch(local_c) {
    case 0:
      *(uint *)(local_8 + 0x38) = (DAT_005ff720 != 0) + 1;
      *(undefined4 *)(local_8 + 0x34) = 0;
      *(int *)(local_8 + 0x30) = *(int *)(local_8 + 0x30) + 1;
      break;
    case 1:
      *(int *)(local_8 + 0x34) = *(int *)(local_8 + 0x34) + 0x180;
      if (0xfeff < *(int *)(local_8 + 0x34)) {
        *(undefined4 *)(local_8 + 0x34) = 0xff00;
        *(int *)(local_8 + 0x30) = *(int *)(local_8 + 0x30) + 1;
      }
      break;
    case 2:
      if ((*(uint *)(DAT_007a49fc + 0x1990) & 1) != 0) {
        FUN__text__004db2b0(5);
        *(int *)(local_8 + 0x30) = *(int *)(local_8 + 0x30) + 1;
      }
      break;
    case 3:
      *(int *)(local_8 + 0x34) = *(int *)(local_8 + 0x34) + -0x180;
      if (*(int *)(local_8 + 0x34) < 0x181) {
        *(undefined4 *)(local_8 + 0x34) = 0;
        *(int *)(local_8 + 0x30) = *(int *)(local_8 + 0x30) + 1;
      }
      break;
    case 4:
      local_8 = 0x430203;
      FUN__text__0056ce80();
      return;
    }
    FUN__text__00430220();
    FUN__text__00422360(0);
  } while( true );
}

