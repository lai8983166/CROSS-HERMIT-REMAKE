
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4 FUN__text__0052c643(undefined4 param_1,undefined4 param_2)

{
  undefined1 *puVar1;
  undefined1 uVar2;
  int iVar3;
  uint uVar4;
  int iVar5;
  undefined4 uVar6;
  int iVar7;
  undefined8 uVar8;
  undefined1 auStack_158 [256];
  undefined8 local_58;
  double local_50;
  undefined4 local_48;
  undefined4 local_44;
  int local_40 [2];
  int *local_38;
  int local_34;
  int local_30;
  int local_2c;
  int local_28;
  int local_24;
  int local_20;
  uint local_1c;
  int local_18;
  int local_14;
  uint local_10;
  int local_c;
  int local_8;
  
  local_8 = 0;
  local_c = 0;
  local_20 = 0;
  iVar3 = FUN__text__00546612();
  if (iVar3 != 0) {
    return 0x80004005;
  }
  local_8 = FUN__text__0054389a("1.0.5",0,&LAB__text__0052c636);
  if ((local_8 == 0) || (local_c = FUN__text__0054674c(), local_c == 0)) goto LAB__text__0052caa6;
  iVar3 = __setjmp3(local_8);
  if (iVar3 == 0) {
    local_48 = param_1;
    local_44 = param_2;
    uVar8 = CONCAT44(&LAB__text__0052c5f3,&local_48);
    iVar3 = local_8;
    FUN__text__005465a0();
    FUN__text__00543a5d(local_8,local_c,iVar3,uVar8);
    FUN__text__005443d3(local_8,local_c,&local_34,&local_1c,&local_28,&local_30,0,0,0);
    if (local_30 == 0) {
      *local_38 = 0x32;
    }
    else if (local_30 == 2) {
      *local_38 = 0x14;
    }
    else if (local_30 == 3) {
      *local_38 = 0x29;
    }
    else if (local_30 == 4) {
      *local_38 = 0x33;
    }
    else if (local_30 == 6) {
      *local_38 = 0x15;
    }
    if (local_28 == 0x10) {
      FUN__text__00544547();
      iVar3 = *local_38;
      if (iVar3 == 0x14) {
        *local_38 = 0x36315220;
      }
      else if (iVar3 == 0x15) {
        *local_38 = 0x36315241;
      }
      else if (iVar3 == 0x32) {
        *local_38 = 0x36314c20;
      }
      else {
        if (iVar3 != 0x33) {
          return 0x80004005;
        }
        *local_38 = 0x36314c41;
      }
    }
    if (local_28 < 8) {
      FUN__text__00544559();
    }
    if ((local_30 == 0) && (local_28 < 8)) {
      FUN__text__00544e00();
    }
    iVar3 = FUN__text__005443a8();
    if (iVar3 == 0) {
      iVar3 = FUN__text__0054437f();
      if (iVar3 != 0) {
        FUN__text__00544db8(local_8,_DAT_005d0df8,local_58);
      }
    }
    else {
      FUN__text__005464ca();
    }
    if ((*local_38 != 0x29) && (iVar3 = FUN__text__00544323(), iVar3 != 0)) {
      FUN__text__00544e09();
      iVar3 = *local_38;
      if (iVar3 == 0x14) {
        *local_38 = 0x15;
      }
      else if (iVar3 == 0x32) {
        *local_38 = 0x33;
      }
      else if (iVar3 == 0x36314c20) {
        *local_38 = 0x36314c41;
      }
      else if (iVar3 == 0x36315220) {
        *local_38 = 0x36315241;
      }
    }
    iVar3 = *local_38;
    if ((((iVar3 == 0x14) || (iVar3 == 0x36315220)) || (iVar3 == 0x15)) || (iVar3 == 0x36315241)) {
      FUN__text__0054453e();
    }
    if (*local_38 == 0x14) {
      FUN__text__005445a4();
      *local_38 = 0x16;
    }
    FUN__text__00543bd0();
    iVar3 = *local_38;
    uVar4 = 3;
    if (iVar3 < 0x34) {
      if (iVar3 == 0x33) {
LAB__text__0052c916:
        local_10 = 2;
        uVar4 = local_10;
      }
      else if (iVar3 != 0x14) {
        if ((iVar3 == 0x15) || (iVar3 == 0x16)) {
LAB__text__0052c90c:
          uVar4 = 4;
        }
        else if ((iVar3 == 0x29) || (uVar4 = local_10, iVar3 == 0x32)) goto LAB__text__0052c8d2;
      }
    }
    else if (iVar3 == 0x36314c20) {
LAB__text__0052c8d2:
      local_10 = 1;
      uVar4 = local_10;
    }
    else {
      if (iVar3 == 0x36314c41) goto LAB__text__0052c916;
      if ((iVar3 != 0x36315220) && (uVar4 = local_10, iVar3 == 0x36315241))
      goto LAB__text__0052c90c;
    }
    local_10 = uVar4;
    uVar4 = FUN__text__00544353(local_8,local_c);
    if (local_10 == (uVar4 & 0xff)) {
      local_38[3] = local_34;
      local_38[4] = local_1c;
      local_38[5] = 1;
      iVar3 = FUN__text__0054433d(local_8,local_c);
      local_38[0xc] = iVar3;
      local_38[0xd] = 0;
      if (local_38[0x10] == 0) goto LAB__text__0052cba8;
      iVar3 = FUN__text__00428a40();
      local_38[1] = iVar3;
      if (iVar3 != 0) {
        local_38[0xe] = 1;
        local_20 = FUN__text__00428a40();
        if (local_20 != 0) {
          uVar4 = 0;
          if (local_1c != 0) {
            do {
              *(uint *)(local_20 + uVar4 * 4) = local_38[0xc] * uVar4 + local_38[1];
              uVar4 = uVar4 + 1;
            } while (uVar4 < local_1c);
          }
          FUN__text__00544023(local_8,local_20);
          if (*local_38 == 0x29) {
            local_2c = 0;
            local_24 = 0;
            iVar3 = FUN__text__00544323();
            if (iVar3 != 0) {
              FUN__text__005444a4(local_8,local_c,&local_14,&local_24);
            }
            iVar3 = FUN__text__00544323();
            if (iVar3 != 0) {
              FUN__text__005444d7(local_8,local_c,local_40,&local_2c,0);
            }
            if ((*(float *)(local_8 + 0x130) <= (float)_DAT_005d0df0) ||
               (*(float *)(local_8 + 0x134) <= (float)_DAT_005d0df0)) {
              iVar3 = 0;
              do {
                auStack_158[iVar3] = (char)iVar3;
                iVar3 = iVar3 + 1;
              } while (iVar3 < 0x100);
            }
            else {
              local_18 = 0;
              local_50 = (double)((float)_DAT_005d0de8 /
                                 (*(float *)(local_8 + 0x134) * *(float *)(local_8 + 0x130)));
              do {
                FUN__text__00571ba0();
                uVar2 = __ftol();
                iVar3 = local_18 + 1;
                puVar1 = auStack_158 + local_18;
                local_18 = iVar3;
                *puVar1 = uVar2;
              } while (iVar3 < 0x100);
            }
            iVar3 = FUN__text__00428a40();
            local_38[2] = iVar3;
            if (iVar3 == 0) goto LAB__text__0052caa6;
            iVar3 = 0;
            local_38[0xf] = 1;
            if (0 < local_2c) {
              iVar7 = 0;
              do {
                iVar5 = iVar3 * 4;
                *(undefined1 *)(iVar5 + local_38[2]) = auStack_158[*(byte *)(iVar7 + local_14)];
                *(undefined1 *)(local_38[2] + 1 + iVar5) =
                     auStack_158[*(byte *)(iVar7 + 1 + local_14)];
                *(undefined1 *)(local_38[2] + 2 + iVar5) =
                     auStack_158[*(byte *)(iVar7 + 2 + local_14)];
                puVar1 = (undefined1 *)(iVar3 + local_40[0]);
                iVar3 = iVar3 + 1;
                *(undefined1 *)(local_38[2] + 3 + iVar5) = *puVar1;
                iVar7 = iVar7 + 3;
              } while (iVar3 < local_2c);
            }
            if (iVar3 < local_24) {
              iVar7 = iVar3 * 3;
              do {
                iVar5 = iVar3 * 4;
                *(undefined1 *)(iVar5 + local_38[2]) = auStack_158[*(byte *)(iVar7 + local_14)];
                *(undefined1 *)(local_38[2] + 1 + iVar5) =
                     auStack_158[*(byte *)(iVar7 + 1 + local_14)];
                *(undefined1 *)(local_38[2] + 2 + iVar5) =
                     auStack_158[*(byte *)(iVar7 + 2 + local_14)];
                *(undefined1 *)(local_38[2] + 3 + iVar5) = 0xff;
                iVar3 = iVar3 + 1;
                iVar7 = iVar7 + 3;
              } while (iVar3 < local_24);
            }
            if (iVar3 < 0x100) {
              iVar3 = iVar3 << 2;
              do {
                *(undefined1 *)(iVar3 + local_38[2]) = 0xff;
                *(undefined1 *)(iVar3 + 1 + local_38[2]) = 0xff;
                *(undefined1 *)(iVar3 + 2 + local_38[2]) = 0xff;
                *(undefined1 *)(iVar3 + 3 + local_38[2]) = 0xff;
                iVar3 = iVar3 + 4;
              } while (iVar3 < 0x400);
            }
          }
LAB__text__0052cba8:
          uVar6 = 0;
          goto LAB__text__0052cbaa;
        }
      }
LAB__text__0052caa6:
      uVar6 = 0x8007000e;
      goto LAB__text__0052cbaa;
    }
  }
  uVar6 = 0x80004005;
LAB__text__0052cbaa:
  if (local_8 != 0) {
    FUN__text__005442a2();
  }
  if (local_20 != 0) {
    FUN__text__00428ad0();
  }
  return uVar6;
}

