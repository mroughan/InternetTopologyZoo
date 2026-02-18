// $Id: tabs.js,v 1.4 2008/04/14 18:35:30 nedjo Exp $

Drupal.behaviors.tabs = function (context) {

  var fx = {duration: Drupal.settings.tabs.speed};
  if (Drupal.settings.tabs.fade) {
    fx.opacity = 'toggle';
  }
  if (Drupal.settings.tabs.slide) {
    fx.height = 'toggle';
  }
  // Process custom tabs.
  $('.drupal-tabs:not(.tabs-processed)', context)
    .addClass('tabs-processed')
    .each(function () {
      if ($(this).is('.tabs-navigation')) {
        Drupal.tabsNavigation(this);
      }
    })
    .find('> ul')
    .tabs({
      selectedClass: 'active',
      fx: fx
    })
    .addClass('tabs')
    .each(function () {
      // Assign secondary class to nested tabsets.
      var newClass = $(this).parents('.drupal-tabs').size() > 1 ? 'secondary' : 'primary';
      $(this).addClass(newClass);
    })
    .after('<span class="clear"></span>')
    .end()
    .show();
};

Drupal.tabsNavigation = function(elt) {
  // Extract tabset name
  var tabsetName = $(elt).get(0).id.substring(5);
  var count = $(elt).find('> ul > li').size();
  var $tabs = $(elt).tabs();
  for (i = 1; i <= count; i++) {
    var tabContent = $('#tabs-' + tabsetName + '-' + i);
    if ((i > 1) || (i < count)) {
      tabContent.append('<span class="clear"></span><div class="tabs-nav-link-sep"></div>');
    }
    if (i > 1) {
      var link = $(document.createElement('a'))
        .append(Drupal.settings.tabs.previous_text)
        .attr('id', 'tabs-' + tabsetName + '-previous-link-' + i)
        .addClass('tabs-nav-previous')
        .click(function() {
          var tabIndex = parseInt($(this).attr('id').substring($(this).attr('id').lastIndexOf('-') + 1)) -1;
          $tabs.tabs('select', tabIndex - 1);
          //Drupal.scrollTo(elt);
          return false;
        });
      tabContent.append(link);
    }
    if (i < count) {
      var link = $(document.createElement('a'))
        .append(Drupal.settings.tabs.next_text)
        .attr('id', 'tabs-' + tabsetName + '-next-button-' + i)
        .addClass('tabs-nav-next')
        .click(function() {
          var tabIndex = parseInt($(this).attr('id').substring($(this).attr('id').lastIndexOf('-') + 1)) -1;
          $tabs.tabs('select', tabIndex + 1);
          //Drupal.scrollTo(elt);
          return false;
        });
      tabContent.append(link);
    }
    tabContent.append('<span class="clear"></span>')
  }
}

Drupal.tabsLocalTasks = function(elt) {
  var elt = elt ? elt : document;
  // Process standard Drupal local task tabs.
  // Only proceed if we have dynamicload available.
  if (Drupal.settings && Drupal.settings.tabs && Drupal.dynamicload && typeof(Drupal.dynamicload == 'function')) {

    $(elt).find('ul.tabs.primary')
      .each(function() {
        var index = 1;
        var activeIndex;
        $(this)
        .addClass('tabs-processed')
        .find('li > a')
        .each(function () {
          var div = document.createElement('div');
          $(div)
            .attr('id', 'section-' + index)
            .addClass('fragment');
          var parentDiv = $(this).parents('div').get(0);
          parentDiv.appendChild(div);
          // The active tab already has content showing.
          if ($(this).is('.active')) {
            activeIndex = parseInt(index);
          }
          // Other tabs need to load their content.
          else {
            Drupal.dynamicload(this, {
              target: document.getElementById('section-' + index),
              useClick: false,
              show: false
            });
          }
          $(this).attr('href', '#section-' + index);
          index++;
        })
        .end()
        .parent('div')
        .each(function() {
          while (this.nextSibling) {
            var oldDiv = this.parentNode.removeChild(this.nextSibling);
            document.getElementById('section-' + activeIndex).appendChild(oldDiv);
          }
        })
        .tabs({
          onShow: Drupal.tabsAddClassesCallback()
        });
    });
  }
};
